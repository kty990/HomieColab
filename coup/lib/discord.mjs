import Discord from 'discord.js';
import { Guild } from 'discord.js';
import { assert } from './util.mjs';

class DiscordBot {
    constructor(token = "") {
        this.token = token;
        this.client = new Discord.Client({
            partials: [Partials.Message, Partials.Channel, Partials.Reaction],
            intents: [
                Intents.DirectMessages,
                Intents.DirectMessageReactions,
                Intents.GuildMessages,
                Intents.GuildMessageReactions,
                Intents.GuildMembers,
                Intents.GuildPresences,
                Intents.Guilds,
                Intents.MessageContent,
                Intents.GuildVoiceStates
            ],
        });
    }

    SendMessage(channel = null, content = "") {
        assert(channel != null, "Can't send message to null channel.");
    }
}