import axios from "axios";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
const TOKEN_FILE = path.join(__dirname, "../../.tokens.json");

async function main() {
    const workflowId = process.argv[2];
    if (!workflowId) {
        console.error("Please provide a workflow ID as an argument.");
        process.exit(1);
    }

    if (!fs.existsSync(TOKEN_FILE)) {
        console.error("Tokens file not found. Please authenticate first.");
        process.exit(1);
    }

    const tokens = JSON.parse(fs.readFileSync(TOKEN_FILE, "utf-8"));
    const accessToken = tokens.access_token;

    try {
        console.log(`Fetching workflow details for ID: ${workflowId}...`);
        
        const response = await axios.get(
            `https://services.leadconnectorhq.com/workflows/?locationId=${LOCATIONimport axios from "axios";
import fs from "fs";
import path from "path";
import n:import fs from "fs";
impo
 import path from "pVersion: "2021-07-28"
     
dotenv.config({ path: path   
const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
const TOKEN_FI
        const targetWorkflow = workflows.find(
async function main() {
    const workflowId = process.argv[ow)    const workflowId =.l    if (!workflowId) {
        console          console.errors:        process.exit(1);
    }

    if (!fs.existsSync(TOKEN_FILE)) {Wo    }

    if (!fs.exis  
   con        console.error("Tokens file now        process.exit(1);
    }

    const tokens = JSON.parse(fs.readFileS${    }

    con" not foun