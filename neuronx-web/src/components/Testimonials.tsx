import { Avatar, AvatarFallback } from "./ui/avatar";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollReveal, StaggerContainer, StaggerItem } from "./ui/scroll-reveal";

interface TestimonialProps {
  name: string;
  userName: string;
  comment: string;
}

const testimonials: TestimonialProps[] = [
  {
    name: "Rajiv M.",
    userName: "RCIC, Express Entry Specialist",
    comment:
      "Before NeuronX, I was losing 40% of my leads to slow follow-up. Now every inquiry gets a call within 5 minutes and I walk into every consultation fully prepared. Three new retainers in the first month alone.",
  },
  {
    name: "Priya K.",
    userName: "Managing Partner, Immigration Law",
    comment:
      "The pre-consultation briefings are game-changing. My RCICs used to spend 30 minutes prepping for each meeting. NeuronX does it automatically. We handle 2x the consultations with the same team.",
  },
  {
    name: "David P.",
    userName: "Intake Coordinator",
    comment:
      "I used to manage leads in spreadsheets and hope I didn't forget anyone. NeuronX's pipeline shows me exactly who to follow up with, when, and why. No lead falls through the cracks.",
  },
  {
    name: "Nina S.",
    userName: "Firm Owner, 8-person Practice",
    comment:
      "We switched from CaseEasy for intake. CaseEasy is great for case management, but NeuronX owns the funnel that feeds us clients. Together they're unbeatable. ROI was clear in week two.",
  },
  {
    name: "Ahmed H.",
    userName: "RCIC, Spousal Sponsorship",
    comment:
      "The AI compliance guardrails give me peace of mind. It never promises outcomes or assesses eligibility. It just collects the right information and books the right people. That's exactly what I need.",
  },
  {
    name: "Sarah L.",
    userName: "Business Development Lead",
    comment:
      "We finally have visibility into our conversion funnel. I can see which programs convert best, which lead sources have the highest ROI, and where prospects get stuck. Data-driven immigration consulting.",
  },
];

const avatarColors = [
  "bg-[#4F46E5]", "bg-[#7C3AED]", "bg-[#2563EB]",
  "bg-[#7C3AED]", "bg-[#4F46E5]", "bg-[#2563EB]",
];

export const Testimonials = () => {
  return (
    <section id="testimonials" className="container py-14 sm:py-16">
      <ScrollReveal>
        <h2 className="text-3xl md:text-4xl font-bold text-center">
          Why Immigration Firms{" "}
          <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
            Choose NeuronX
          </span>
        </h2>

        <p className="text-xl text-muted-foreground pt-4 pb-8 text-center max-w-2xl mx-auto">
          From solo practitioners to multi-RCIC firms — NeuronX transforms how
          Canadian immigration consultancies convert and retain clients.
        </p>
      </ScrollReveal>

      <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {testimonials.map(
          ({ name, userName, comment }: TestimonialProps, idx) => (
            <StaggerItem key={userName}>
              <Card className="h-full hover:-translate-y-2 hover:scale-[1.01] transition-all duration-300 hover:shadow-lg hover:shadow-primary/5">
                <CardHeader className="flex flex-row items-center gap-4 pb-2">
                  <Avatar className="w-11 h-11">
                    <AvatarFallback className={`${avatarColors[idx]} text-white font-bold text-sm`}>
                      {name.split(" ").map((n) => n[0]).join("")}
                    </AvatarFallback>
                  </Avatar>

                  <div className="flex flex-col">
                    <CardTitle className="text-lg">{name}</CardTitle>
                    <CardDescription>{userName}</CardDescription>
                  </div>
                </CardHeader>

                <CardContent className="text-sm leading-relaxed text-muted-foreground">
                  {comment}
                </CardContent>
              </Card>
            </StaggerItem>
          )
        )}
      </StaggerContainer>
    </section>
  );
};
