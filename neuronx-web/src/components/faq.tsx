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
    question: "Is the AI giving immigration advice?",
    answer: "Absolutely not. NeuronX's AI collects factual information — program interest, location, timeline, prior history. It never assesses eligibility, recommends pathways, or interprets immigration law. Every conversation is designed within IRCC compliance boundaries, reviewed by a licensed RCIC (R705959).",
    value: "item-1",
  },
  {
    question: "What if a prospect needs a human immediately?",
    answer: "The system escalates instantly. Mentions of deportation, emotional distress, explicit human requests, or any situation outside the AI's scope triggers an immediate handoff to your team with full context. This is a hard-coded safety boundary that cannot be overridden.",
    value: "item-2",
  },
  {
    question: "How long does setup take?",
    answer: "Most firms are live within 48 hours. We configure your account, customize your intake form, connect your calendar, and run a test inquiry end-to-end before you go live. No lengthy implementation or training required.",
    value: "item-3",
  },
  {
    question: "Do I need to change my current case management system?",
    answer: "No. NeuronX handles the pre-retainer funnel — everything from first inquiry to signed retainer. Once a client signs, your existing case management system (CaseEasy, Visto, or manual process) takes over. We fill your pipeline with qualified, briefed clients. We don't replace your case tools.",
    value: "item-4",
  },
  {
    question: "What immigration programs are supported?",
    answer: "All 8 major Canadian programs: Express Entry, Spousal Sponsorship, Work Permit, Study Permit, LMIA, PR Renewal, Citizenship, and Visitor Visa. Each has program-specific intake questions, scoring adjustments, nurture content, and document checklists.",
    value: "item-5",
  },
  {
    question: "What happens after the 14-day pilot?",
    answer: "You keep everything. All leads, scores, bookings, and briefings generated during the pilot are yours. If you don't see value, cancel with one click. No contracts, no penalties, no data hostage.",
    value: "item-6",
  },
  {
    question: "Is my client data secure?",
    answer: "All data is encrypted in transit and at rest, stored on Canadian-compliant infrastructure. We never share client data with third parties. PIPEDA compliant. Your data belongs to you — always.",
    value: "item-7",
  },
  {
    question: "How is NeuronX different from CaseEasy or Visto?",
    answer: "CaseEasy, Visto, and VisaFlo are excellent case management tools for after a client signs. NeuronX handles everything before — the inquiry-to-retainer funnel. Most firms use both: NeuronX gets you clients, case management tools help you serve them.",
    value: "item-8",
  },
];

export const FAQ = () => {
  return (
    <section id="faq" className="container py-16 sm:py-20">
      <h2 className="text-3xl md:text-4xl font-bold mb-4">
        Questions we hear from{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          every firm
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
          Talk to the founders directly
        </a>
      </h3>
    </section>
  );
};
