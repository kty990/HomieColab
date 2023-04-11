import Discord from 'discord.js';
import { Guild } from 'discord.js';
import { assert } from './util.mjs';

class Embed {
    constructor() {
        this.embed = {
            title: "\u2800",
            description: "\u2800",
            fields: [],
            author: {
                name: "embed",
                icon_url: ""
            },
            color: 0xffffff,
            timestamp: new Date().toISOString(),
            footer: {
                text: '\u2800',
                icon_url: '',
            },
        };
    }

    SetTitle(title = "\u2800") {
        this.embed.title = title;
    }

    SetDescription(desc = "\u2800") {
        this.embed.description = desc;
    }

    SetColor(hex = 0xffffff) {
        this.embed.color = hex;
    }

    SetAuthor(name = "embed", icon_url = "") {
        this.embed.author.name = name;
        this.embed.author.icon_url = icon_url;
    }

    SetFooter(text = "embed", icon_url = "") {
        this.embed.author.text = text;
        this.embed.author.icon_url = icon_url;
    }
}

export { Embed }

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
        this.client.login(token);
    }

    SendMessage(channel = null, content = "") {
        assert(channel == null, "Can't send message to null channel.");
        if (content instanceof Embed) {
            channel.send({ embeds: content.embed })
                .catch(console.error);
        } else {
            channel.send(content)
                .catch(console.error);
        }
    }

    // WaitForInput(MESSAGE) << Waits for message to be sent
    async WaitForInput(msg = null) {
        assert(msg == null, "Can't wait for an empty message");
        return new Promise((resolve, reject) => {
            resolve();
        });
    }

    // WaitForInputFromMember(MEMBER)

    // GetEmoji()

    // WaitForReaction(MESSAGE)

    // WaitForReactionFromMember(MESSAGE,MEMBER)

    // WaitForSlashCommand(COMMAND_NAME)

}