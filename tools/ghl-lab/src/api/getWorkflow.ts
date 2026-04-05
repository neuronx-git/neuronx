import axios from "axios";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
const TOKEN_FILE = path.join(__dirname, "../../.tokens.json");

async function main() {
    const workflowName = process.argv[2];
    if (!workflowName) {
        console.error("Please provide a workflow name or ID as an argument.");
        process.exit(1);
    }

    if (!fs.existsSync(TOKEN_FILE)) {
        console.error("Tokens file not found. Please authenticate first.");
        process.exit(1);
    }

    const tokens = JSON.parse(fs.readFileSync(TOKEN_FILE, "utf-8"));
    const accessToken = tokens.access_token;

    try {
        console.log(`Searching for workflow: ${workflowName}...`);
        const response = await axios.get(
            `https://services.leadconnectorhq.com/workflows/?locationId=${LOCATION_ID}`,
            {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                    Version: "2021-07-28"
                }
            }
        );

        const workflows = response.data.workflows;
        const targetWorkflow = workflows.find((wf: any) => wf.name.includes(workflowName) || wf.id === workflowName);

        if (targetWorkflow) {
            console.log("Workflow Found!");
            console.log(JSON.stringify(targetWorkflow, null, 2));
        } else {
            console.error(`Workflow '${workflowName}' not found.`);
            console.log("Available workflows:", workflows.map((wf: any) => wf.name));
        }

    } catch (error: any) {
        console.error("Error fetching workflows:", error.response ? error.response.data : error.message);
    }
}

main();
