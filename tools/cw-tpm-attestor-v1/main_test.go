package main

import (
    "encoding/json"
    "os"
    "path/filepath"
    "strings"
    "testing"
    "time"

    "github.com/google/go-attestation/attest"
)
func TestNonceGenerationAndTimeBounds(t *testing.T) {
    p:=filepath.Join(t.TempDir(),"challenge.json")
    if err:=challenge([]string{"--out",p});err!=nil{t.Fatal(err)}
    c,n,err:=readChallenge(p);if err!=nil{t.Fatal(err)}
    if len(n)!=20||c.Schema!=challengeSchema||len(c.ID)!=64 {t.Fatalf("invalid challenge: %+v",c)}
    if err:=challenge([]string{"--out",p});err==nil {t.Fatal("overwrote challenge")}
    c.ExpiresUTC=time.Now().Add(-time.Minute)
    b,_:=json.Marshal(c);if err:=os.WriteFile(p,b,0600);err!=nil{t.Fatal(err)}
    if _,_,err:=readChallenge(p);err==nil{t.Fatal("accepted expired challenge")}
}
func TestTamperedChallengeRejected(t *testing.T) {
    p:=filepath.Join(t.TempDir(),"challenge.json")
    if err:=challenge([]string{"--out",p});err!=nil{t.Fatal(err)}
    var c Challenge
    if err:=readJSON(p,&c);err!=nil{t.Fatal(err)}
    c.ID=strings.Repeat("0",64)
    b,_:=json.Marshal(c)
    if err:=os.WriteFile(p,b,0600);err!=nil{t.Fatal(err)}
    if _,_,err:=readChallenge(p);err==nil{t.Fatal("challenge ID not bound to nonce")}
}
func TestForgedEvidenceMustFailClosed(t *testing.T) {
    d:=t.TempDir()
    cp,ep,rp:=filepath.Join(d,"challenge.json"),filepath.Join(d,"fake-quote.json"),filepath.Join(d,"verify.json")
    if err:=challenge([]string{"--out",cp});err!=nil{t.Fatal(err)}
    c,_,err:=readChallenge(cp);if err!=nil{t.Fatal(err)}
    e:=Evidence{Schema:schema,ChallengeID:c.ID,CollectedUTC:time.Now(),Platform:attest.PlatformParameters{
      Public:[]byte{1,2,3},Quotes:[]attest.Quote{{Quote:[]byte{9},Signature:[]byte{8}}},PCRs:[]attest.PCR{{Index:7,Digest:[]byte{0,0,0}}},EventLog:[]byte{0,1,2}}}
    e.AKPublicSHA256=digestHex(e.Platform.Public)
    if err:=saveJSON(ep,e);err!=nil{t.Fatal(err)}
    err=verify([]string{"--challenge",cp,"--evidence",ep,"--out",rp,"--spent-dir",filepath.Join(d,"spent")})
    if err==nil {t.Fatal("accepted forged signature or AK")}
    var r Receipt
    if err:=readJSON(rp,&r);err!=nil{t.Fatal(err)}
    if r.Verdict!="FAIL"||r.IndependentHardwareCertification!="UNKNOWN"{t.Fatalf("incorrect verdict: %+v",r)}
    if _,err:=os.Stat(filepath.Join(d,"spent",c.ID+".used"));err==nil {t.Fatal("consumed challenge for invalid quote")}
}
func TestReceiptMustNotOverwrite(t *testing.T){
    p:=filepath.Join(t.TempDir(),"receipt.json")
    if err:=saveJSON(p,struct{A int}{1});err!=nil{t.Fatal(err)}
    if err:=saveJSON(p,struct{A int}{2});err==nil{t.Fatal("receipt overwritten")}
}
