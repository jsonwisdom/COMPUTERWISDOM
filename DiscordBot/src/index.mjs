import "dotenv/config";
import {
  Client,
  GatewayIntentBits,
  REST,
  Routes,
  SlashCommandBuilder,
} from "discord.js";
import OpenAI from "openai";
import {
  AUTHORITY,
  SYSTEM_INSTRUCTIONS,
  enforceAuthorityFalse,
  normalizePrompt,
} from "./policy.mjs";

const required = [
  "DISCORD_TOKEN",
  "DISCORD_APPLICATION_ID",
  "DISCORD_GUILD_ID",
  "OPENAI_API_KEY",
];

const missing = required.filter((name) => !process.env[name]);
if (missing.length) {
  throw new Error(`Missing environment variables: ${missing.join(", ")}`);
}

const model = process.env.OPENAI_MODEL || "gpt-5.6";
const openai = new OpenAI();
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const commands = [
  new SlashCommandBuilder()
    .setName("ask")
    .setDescription("Ask JSONWisdom without creating authority")
    .addStringOption((option) =>
      option
        .setName("prompt")
        .setDescription("Question or work item")
        .setRequired(true),
    ),
].map((command) => command.toJSON());

async function registerCommands() {
  const rest = new REST({ version: "10" }).setToken(process.env.DISCORD_TOKEN);
  await rest.put(
    Routes.applicationGuildCommands(
      process.env.DISCORD_APPLICATION_ID,
      process.env.DISCORD_GUILD_ID,
    ),
    { body: commands },
  );
}

client.once("ready", () => {
  console.log(`DiscordBot ready as ${client.user.tag}; authority=${AUTHORITY}`);
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isChatInputCommand() || interaction.commandName !== "ask") return;

  const prompt = normalizePrompt(interaction.options.getString("prompt", true));
  if (!prompt) {
    await interaction.reply({ content: "Empty prompt. authority=false", ephemeral: true });
    return;
  }

  await interaction.deferReply();

  try {
    const response = await openai.responses.create({
      model,
      instructions: SYSTEM_INSTRUCTIONS,
      input: prompt,
      store: false,
    });
    const output = enforceAuthorityFalse(response.output_text).slice(0, 2000);
    await interaction.editReply(output);
  } catch (error) {
    console.error("DiscordBot request failed", error?.request_id ?? error?.name ?? "error");
    await interaction.editReply("Request failed. No action taken. authority=false");
  }
});

await registerCommands();
await client.login(process.env.DISCORD_TOKEN);
