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
    /**
     * 
     * @param {*} msg 
     * @returns Promise
     * 
     * 60 second timelimit, rejects if time expires
     */
    async WaitForInput(msg = null) {
        assert(msg == null, "Can't wait for an empty message");
        return new Promise((resolve, reject) => {
            const filter = m => m.content.toLowerCase() == msg.toLowerCase();
            // Errors: ['time'] treats ending because of the time limit as an error
            channel.awaitMessages({ filter, max: 1, time: 60_000, errors: ['time'] })
                .then(collected => {
                    resolve(collected);
                })
                .catch(() => {
                    reject(`No input matching ${msg} was found within the past 60 seconds`);
                });
        });
    }

    // WaitForInputFromMember(MEMBER)
    /**
     * 
     * @param {*} msg 
     * @returns Promise
     * 
     * 60 second timelimit, rejects if time expires
     */
    async WaitForInputFromMember(mmbr = null) {
        assert(!mmbr instanceof Discord.GuildMember, "Can't wait for an empty member");
        return new Promise((resolve, reject) => {
            const filter = m => m.member.toLowerCase() == msg.toLowerCase();
            // Errors: ['time'] treats ending because of the time limit as an error
            channel.awaitMessages({ filter, max: 1, time: 60_000, errors: ['time'] })
                .then(collected => {
                    resolve(collected);
                })
                .catch(collected => {
                    reject(`No input with user matching ${mmbr.user.tag} was found within the past 60 seconds`);
                });
        });
    }

    // GetEmoji()

    // WaitForReaction(MESSAGE)

    // WaitForReactionFromMember(MESSAGE,MEMBER)

    // WaitForSlashCommand(COMMAND_NAME)

}