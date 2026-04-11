import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

interface FAQProps {
  question: string;
  answer: string;
  value: string;
}

const FAQList: FAQProps[] = [
  {
    question: "Does NeuronX replace our CRM?",
    answer: "No. NeuronX works on top of GoHighLevel (GHL), which serves as your CRM. NeuronX is the intelligence layer — it handles AI calling, scoring, briefings, and analytics. GHL handles contacts, pipelines, email/SMS, and workflows. Together they form a complete system.",
    value: "item-1",
  },
  {
    question: "Is the AI compliant with RCIC regulations?",
    answer: "Yes. NeuronX enforces strict trust boundaries. The AI never assesses immigration eligibility, recommends pathways, interprets law, or promises outcomes. It only collects information, asks factual questions, and books consultations. Every AI interaction is auditable and logged for compliance.",
    value: "item-2",
  },
  {
    question: "How long does onboarding take?",
    answer: "2-4 hours. We install a pre-configured snapshot into your GHL account, customize branding, configure your RCIC team, and run a live test. Your firm is operational the same day. No lengthy implementation or training required.",
    value: "item-3",
  },
  {
    question: "What if a prospect asks the AI for legal advice?",
    answer: "The AI immediately escalates. If a prospect asks about eligibility, mentions deportation, shows emotional distress, or involves a minor, the call is flagged for human follow-up. Your team gets an instant alert. This is a hard-coded safety boundary that cannot be overridden.",
    value: "item-4",
  },
  {
    question: "How does NeuronX compare to CaseEasy or Visto?",
    answer: "CaseEasy, Visto, and VisaFlo are excellent case management tools for AFTER a client signs. NeuronX handles everything BEFORE — the inquiry-to-retainer funnel. Most firms use NeuronX alongside their case management tool. NeuronX gets you clients; case management tools help you serve them.",
    value: "item-5",
  },
  {
    question: "What immigration programs are supported?",
    answer: "All 8 major Canadian programs: Express Entry, Spousal Sponsorship, Work Permit, Study Permit, LMIA, PR Renewal, Citizenship, and Visitor Visa. Each has program-specific intake questions, nurture content, and document checklists.",
    value: "item-6",
  },
  {
    question: "What's the ROI on NeuronX?",
    answer: "One additional retained client ($3,000-$5,000 CAD) pays for 6+ months of NeuronX at the Essentials tier. Most firms see ROI in the first 2-4 weeks. The system pays for itself by converting leads you were already paying to acquire but losing to slow follow-up.",
    value: "item-7",
  },
];

export const FAQ = () => {
  return (
    <section id="faq" className="container py-24 sm:py-32">
      <h2 className="text-3xl md:text-4xl font-bold mb-4">
        Frequently Asked{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          Questions
        </span>
      </h2>

      <Accordion type="single" collapsible className="w-full AccordionRoot">
        {FAQList.map(({ question, answer, value }: FAQProps) => (
          <AccordionItem key={value} value={value}>
            <AccordionTrigger className="text-left">{question}</AccordionTrigger>
            <AccordionContent>{answer}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>

      <h3 className="font-medium mt-4">
        Still have questions?{" "}
        <a
          href="mailto:hello@neuronx.co"
          className="text-primary transition-all border-primary hover:border-b-2"
        >
          Contact us
        </a>
      </h3>
    </section>
  );
};
