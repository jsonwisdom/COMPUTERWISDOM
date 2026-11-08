// Computer Wisdom TPM Attestor v0.1 — evidence-only CLI.
// Uses github.com/google/go-attestation (Windows Platform Crypto Provider).
// NO TPM key is created by default. "enroll" requires --allow-create-ak.
package main

import (
    "crypto/rand"
    "crypto/sha256"
    "crypto/subtle"
    "encoding/hex"
    "encoding/json"
    "errors"
    "flag"
    "fmt"
    "io"
    "os"
    "path/filepath"
    "runtime"
    "strings"
    "time"

    "github.com/google/go-attestation/attest"
)

const schema = "CW_TPM_QUOTE_V1"
const challengeSchema = "CW_TPM_CHALLENGE_V1"
const receiptSchema = "CW_TPM_VERIFY_RECEIPT_V1"
const maxInputBytes = 16 << 20 // avoid unlimited JSON/EventLog allocations

type Challenge struct {
    Schema string `json:"schema"`
    ID string `json:"challenge_id"`
    NonceHex string `json:"nonce_hex"`
    IssuedUTC time.Time `json:"issued_utc"`
    ExpiresUTC time.Time `json:"expires_utc"`
}
type Evidence struct {
    Schema string `json:"schema"`
    ChallengeID string `json:"challenge_id"`
    CollectedUTC time.Time `json:"collected_utc"`
    AKPublicSHA256 string `json:"ak_public_sha256"`
    Platform attest.PlatformParameters `json:"platform"`
}
type Receipt struct {
    Schema string `json:"schema"`
    VerifiedUTC time.Time `json:"verified_utc"`
    ChallengeID string `json:"challenge_id"`
    AKPublicSHA256 string `json:"ak_public_sha256,omitempty"`
    Nonce string `json:"nonce_binding"`
    QuoteSignatureAndPCR string `json:"quote_signature_and_pcr"`
    EventLogReplay string `json:"measured_boot_log_replay"`
    AKPin string `json:"trusted_ak_pin"`
    ReplayPrevention string `json:"nonce_one_time_use"`
    EKToAKBinding string `json:"ek_to_ak_binding"`
    EKRootTrust string `json:"ek_root_trust"`
    BootPolicy string `json:"approved_boot_policy"`
    IndependentHardwareCertification string `json:"independent_hardware_certification"`
    Verdict string `json:"verdict"`
    Error string `json:"error,omitempty"`
}
func readJSON(path string, dst any) error {
    f, err := os.Open(path)
    if err != nil { return err }
    defer f.Close()
    st, err := f.Stat()
    if err != nil { return err }
    if st.Size() > maxInputBytes { return fmt.Errorf("input exceeds %d bytes", maxInputBytes) }
    dec := json.NewDecoder(io.LimitReader(f, maxInputBytes+1))
    dec.DisallowUnknownFields()
    if err := dec.Decode(dst); err != nil { return err }
    var extra any
    if err := dec.Decode(&extra); err != io.EOF { return fmt.Errorf("unexpected trailing JSON: %v", err) }
    return nil
}
func saveExclusive(path string, contents []byte) error {
    // Avoid replacing pre-existing evidence, even on failed verifications.
    f, err := os.OpenFile(path, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0600)
    if err != nil { return err }
    defer f.Close()
    if _, err := f.Write(contents); err != nil { return err }
    return f.Sync()
}
func saveJSON(path string, data any) error {
    b, err := json.MarshalIndent(data, "", "  ")
    if err != nil { return err }
    return saveExclusive(path, append(b, '\n'))
}
func digestHex(b []byte) string { s:=sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func readChallenge(path string) (Challenge, []byte, error) {
    var c Challenge
    if err:=readJSON(path,&c);err!=nil{return c,nil,err}
    if c.Schema!=challengeSchema || c.ID=="" {return c,nil,errors.New("invalid challenge schema/id")}
    n,err:=hex.DecodeString(c.NonceHex)
    if err!=nil || len(n)!=20 {return c,nil,errors.New("challenge must contain exactly 20 random nonce bytes")}
    if c.IssuedUTC.IsZero()||c.ExpiresUTC.IsZero()||c.ExpiresUTC.Sub(c.IssuedUTC)>10*time.Minute||c.ExpiresUTC.Sub(c.IssuedUTC)<=0 {return c,nil,errors.New("invalid challenge time window")}
    now:=time.Now().UTC()
    if now.Before(c.IssuedUTC.Add(-30*time.Second)) || !now.Before(c.ExpiresUTC) {return c,nil,errors.New("challenge not yet valid or expired")}
    if c.ID!=digestHex(n) {return c,nil,errors.New("challenge ID does not match nonce")}
    return c,n,nil
}
func preflight(_ []string) error {
    if runtime.GOOS!="windows" {return errors.New("probe requires Windows with TPM 2.0")}
    t,err:=attest.OpenTPM(nil);if err!=nil{return fmt.Errorf("TPM unavailable: %w",err)}
    defer t.Close()
    info,err:=t.Info();if err!=nil{return err}
    banks,err:=t.PCRBanks();if err!=nil{return err}
    return json.NewEncoder(os.Stdout).Encode(struct{
        Schema string `json:"schema"`
        TPMPresent bool `json:"tpm_open"`
        Manufacturer string `json:"manufacturer"`
        FirmwareMajor int `json:"firmware_major"`
        FirmwareMinor int `json:"firmware_minor"`
        PCRBankCount int `json:"pcr_bank_count"`
        SignedQuoteVerified bool `json:"signed_quote_verified"`
    }{"CW_TPM_PROBE_V1",true,info.Manufacturer.String(),info.FirmwareVersionMajor,info.FirmwareVersionMinor,len(banks),false})
}
func challenge(args []string) error {
    fs:=flag.NewFlagSet("challenge",flag.ContinueOnError)
    out:=fs.String("out","","path to new challenge JSON on verifier")
    if err:=fs.Parse(args);err!=nil{return err}
    if *out=="" {return errors.New("--out required")}
    nonce:=make([]byte,20)
    if _,err:=rand.Read(nonce);err!=nil{return err}
    now:=time.Now().UTC()
    c:=Challenge{Schema:challengeSchema,ID:digestHex(nonce),NonceHex:hex.EncodeToString(nonce),IssuedUTC:now,ExpiresUTC:now.Add(5*time.Minute)}
    if err:=saveJSON(*out,c);err!=nil{return err}
    fmt.Printf("PASS CHALLENGE_CREATED %s (expires %s)\n",*out,c.ExpiresUTC.Format(time.RFC3339))
    return nil
}
func enroll(args []string) error {
    if runtime.GOOS!="windows" {return errors.New("enroll requires Windows")}
    fs:=flag.NewFlagSet("enroll",flag.ContinueOnError)
    allow:=fs.Bool("allow-create-ak",false,"explicitly authorize creation of a persistent Windows PCP attestation key")
    out:=fs.String("out","","new private local opaque AK handle file, never upload")
    if err:=fs.Parse(args);err!=nil{return err}
    if !*allow {return errors.New("REFUSED: --allow-create-ak required; key creation changes persistent Windows PCP state")}
    if *out=="" {return errors.New("--out required")}
    if _,err:=os.Stat(*out);err==nil {return errors.New("REFUSED: AK handle file exists; no overwrite")}
    t,err:=attest.OpenTPM(nil);if err!=nil{return err}
    defer t.Close()
    a,err:=t.NewAK(nil)
    if err!=nil {return fmt.Errorf("creating persistent TPM attestation key: %w",err)}
    defer a.Close(t)
    opaque,err:=a.Marshal();if err!=nil{return fmt.Errorf("AK created but handle save failed: %w",err)}
    if err:=saveExclusive(*out,opaque);err!=nil{return fmt.Errorf("AK created but handle save failed; keep audit trail: %w",err)}
    fmt.Printf("PASS AK_CREATED_AND_HANDLE_SAVED %s\nThe Windows PCP key persists; private key is not exported. This is NOT an EK-bound trusted identity.\n",*out)
    return nil
}
func quote(args []string) error {
    if runtime.GOOS!="windows" {return errors.New("quote requires Windows")}
    fs:=flag.NewFlagSet("quote",flag.ContinueOnError)
    challengePath:=fs.String("challenge","","challenge file issued by verifier")
    akPath:=fs.String("ak","","existing local AK handle from enroll")
    out:=fs.String("out","","new private quote evidence JSON")
    if err:=fs.Parse(args);err!=nil{return err}
    if *out==""||*challengePath==""||*akPath=="" {return errors.New("--challenge, --ak and --out required")}
    c,nonce,err:=readChallenge(*challengePath);if err!=nil{return err}
    akBlob,err:=os.ReadFile(*akPath);if err!=nil{return err}
    if len(akBlob)==0||len(akBlob)>65536 {return errors.New("invalid AK handle size")}
    t,err:=attest.OpenTPM(nil);if err!=nil{return err}
    defer t.Close()
    ak,err:=t.LoadAK(akBlob);if err!=nil{return fmt.Errorf("loading existing AK: %w",err)}
    defer ak.Close(t)
    platform,err:=t.AttestPlatform(ak,nonce,nil)
    if err!=nil{return fmt.Errorf("TPM quote failed (no receipt created): %w",err)}
    if len(platform.Quotes)==0 || len(platform.Public)==0 {return errors.New("empty platform quote/public key")}
    evidence:=Evidence{Schema:schema,ChallengeID:c.ID,CollectedUTC:time.Now().UTC(),AKPublicSHA256:digestHex(platform.Public),Platform:*platform}
    if err:=saveJSON(*out,evidence);err!=nil{return err}
    fmt.Printf("PASS TPM_QUOTE_CAPTURED %s\nQuote must still be independently verified. Keep PCRs, AK public and event log private.\n",*out)
    return nil
}
func verify(args []string) error {
    fs:=flag.NewFlagSet("verify",flag.ContinueOnError)
    challengePath:=fs.String("challenge","","original challenge on separate verifier")
    evidencePath:=fs.String("evidence","","collected quote JSON")
    out:=fs.String("out","","new verification receipt JSON, never overwritten")
    seenDir:=fs.String("spent-dir","","verifier-controlled private directory for one-time nonce consumption")
    trustedAK:=fs.String("trusted-ak-sha256","","optional 64-digit out-of-band enrolled AK blob SHA-256; does NOT prove EK binding")
    if err:=fs.Parse(args);err!=nil{return err}
    if *challengePath==""||*evidencePath==""||*out=="" {return errors.New("--challenge, --evidence, --out required")}
    r:=Receipt{Schema:receiptSchema,VerifiedUTC:time.Now().UTC(),Nonce:"UNKNOWN",QuoteSignatureAndPCR:"UNKNOWN",EventLogReplay:"UNKNOWN",AKPin:"UNKNOWN",ReplayPrevention:"UNKNOWN",EKToAKBinding:"UNKNOWN",EKRootTrust:"UNKNOWN",BootPolicy:"UNKNOWN",IndependentHardwareCertification:"UNKNOWN",Verdict:"UNKNOWN"}
    var failure error
    c,nonce,err:=readChallenge(*challengePath)
    if err!=nil {failure=fmt.Errorf("challenge: %w",err)} else {r.ChallengeID=c.ID}
    var e Evidence
    if failure==nil {
        if err:=readJSON(*evidencePath,&e);err!=nil{failure=fmt.Errorf("evidence: %w",err)}
    }
    if failure==nil {
        if e.Schema!=schema || e.ChallengeID!=c.ID || len(e.Platform.Quotes)==0 || len(e.Platform.Public)==0 || len(e.Platform.PCRs)==0 {
            failure=errors.New("invalid evidence schema, challenge binding, or quote/PCR contents")
        } else {r.Nonce="PASS"}
    }
    if failure==nil {
        r.AKPublicSHA256=digestHex(e.Platform.Public)
        if e.AKPublicSHA256!=r.AKPublicSHA256 {failure=errors.New("AK public SHA-256 mismatch")}
    }
    if failure==nil && strings.TrimSpace(*trustedAK)!="" {
        pin,err:=hex.DecodeString(strings.TrimSpace(*trustedAK))
        if err!=nil||len(pin)!=32 {failure=errors.New("bad trusted AK pin")} else {
            got,_:=hex.DecodeString(r.AKPublicSHA256)
            if subtle.ConstantTimeCompare(pin,got)!=1 {failure=errors.New("trusted AK pin mismatch");r.AKPin="FAIL"} else {r.AKPin="PASS_PIN_ONLY"}
        }
    }
    if failure==nil {
        pub,err:=attest.ParseAKPublic(e.Platform.Public)
        if err!=nil{failure=fmt.Errorf("AK public key: %w",err)} else if err:=pub.VerifyAll(e.Platform.Quotes,e.Platform.PCRs,nonce);err!=nil{
            failure=fmt.Errorf("TPM quote signature/nonce/PCR binding: %w",err)
        } else {r.QuoteSignatureAndPCR="PASS"}
    }
    if failure==nil {
        log,err:=attest.ParseEventLog(e.Platform.EventLog)
        if err!=nil{failure=fmt.Errorf("measured-boot log parse: %w",err)} else if _,err:=log.Verify(e.Platform.PCRs);err!=nil{
            failure=fmt.Errorf("PCR/event-log replay: %w",err)
        } else {r.EventLogReplay="PASS"}
    }
    if failure==nil && *seenDir!="" {
        if err:=os.MkdirAll(*seenDir,0700);err!=nil {failure=err} else {
            spent:=filepath.Join(*seenDir,c.ID+".used")
            if err:=saveExclusive(spent,[]byte(r.VerifiedUTC.Format(time.RFC3339Nano)+"\n"));err!=nil {
                failure=fmt.Errorf("nonce already consumed or verifier state unavailable: %w",err)
            } else {r.ReplayPrevention="PASS_ONE_TIME"}
        }
    }
    if failure!=nil {
        r.Verdict="FAIL";r.Error=failure.Error()
        if r.QuoteSignatureAndPCR=="UNKNOWN" {r.QuoteSignatureAndPCR="FAIL_OR_NOT_TESTED"}
        if err:=saveJSON(*out,r);err!=nil{return fmt.Errorf("verification failed: %v; also failed to save receipt: %w",failure,err)}
        fmt.Printf("FAIL receipt=%s reason=%s\n",*out,r.Error)
        return failure
    }
    r.Verdict="CRYPTOGRAPHIC_QUOTE_AND_EVENT_LOG_PASS_ONLY"
    if err:=saveJSON(*out,r);err!=nil{return err}
    fmt.Printf("PASS QUOTE_CRYPTO_AND_LOG_REPLAY %s\nUNKNOWN: EK-to-AK identity, trusted AMD root, approved boot baseline and external certification.\n",*out)
    return nil
}
func usage() {
    fmt.Fprintln(os.Stderr,"CW-TPM v0.1 commands: probe | challenge --out FILE | enroll --allow-create-ak --out FILE | quote --ak FILE --challenge FILE --out FILE | verify --challenge FILE --evidence FILE --out FILE [--spent-dir DIR] [--trusted-ak-sha256 HEX]")
}
func main(){
    if len(os.Args)<2 {usage();os.Exit(2)}
    var err error
    switch os.Args[1] {
    case "probe": err=preflight(os.Args[2:])
    case "challenge": err=challenge(os.Args[2:])
    case "enroll": err=enroll(os.Args[2:])
    case "quote": err=quote(os.Args[2:])
    case "verify": err=verify(os.Args[2:])
    default: usage();os.Exit(2)
    }
    if err!=nil {fmt.Fprintf(os.Stderr,"CI-FIRST FAIL: %v\n",err);os.Exit(1)}
}