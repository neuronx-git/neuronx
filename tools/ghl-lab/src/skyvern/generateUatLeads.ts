import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      const url = await agent.createSession();
      console.log("\n!!! ACTION REQUIRED !!!");
      console.log("A new Skyvern session has been created.");
      console.log(`Please open this URL to monitor and LOG IN to GoHighLevel:`);
      console.log(url);
      console.log("\nOnce you have logged in, please run this script again.");
      process.exit(0);
  }

  const FORM_URL = "https://api.leadconnectorhq.com/widget/form/FNMmVXpfUvUypS0c4oQ3";

  const leads = [
      { first: "Test", last: "Express Entry", email: "ee@neuronx.ai", phone: "+15552220001", program: "Express Entry", country: "India", time: "3-6 months" },
      { first: "Test", last: "Student Visa", email: "sv@neuronx.ai", phone: "+15552220002", program: "Study Permit", country: "Philippines", time: "Within 3 months" },
      { first: "Test", last: "PNP", email: "pnp@neuronx.ai", phone: "+15552220003", program: "Provincial Nominee (PNP)", country: "Nigeria", time: "6-12 months" },
      { first: "Test", last: "Family Sponsorship", email: "fs@neuronx.ai", phone: "+15552220004", program: "Family Sponsorship", country: "Other", time: "More than 12 months" }, // Using "Other" as UAE might not be in the dropdown explicitly based on earlier config
      { first: "Test", last: "Visitor Visa", email: "vv@neuronx.ai", phone: "+15552220005", program: "Visitor Visa", country: "Other", time: "Just exploring" } // Using "Other" for Brazil
  ];

  try {
      console.log("Starting UAT Lead Generation...");
      
      const results = [];

      for (const lead of leads) {
          console.log(`Submitting lead: ${lead.last}...`);
          
          const result = await agent.executeStep(
              `
              Navigate to the form.
              Fill out the form with these exact details:
              - First Name: ${lead.first}
              - Last Name: ${lead.last}
              - Email: ${lead.email}
              - Phone: ${lead.phone}
              - Program Interest: ${lead.program}
              - Location: ${lead.country}
              - Timeline: ${lead.time}
              
              Submit the form. Wait for the success message or redirect.
              `,
              FORM_URL
          );
          
          results.push({ lead: lead.last, status: result.status });
          console.log(`Lead ${lead.last} submitted.`);
      }

      console.log("UAT Submission Results:", JSON.stringify(results, null, 2));

  } catch (e) { console.error("Failed", e); }
}

main();
