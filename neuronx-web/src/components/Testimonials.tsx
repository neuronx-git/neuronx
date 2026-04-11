import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface TestimonialProps {
  image: string;
  name: string;
  userName: string;
  comment: string;
}

const testimonials: TestimonialProps[] = [
  {
    image: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7?32",
    name: "Rajiv M.",
    userName: "RCIC, Express Entry Specialist",
    comment:
      "Before NeuronX, I was losing 40% of my leads to slow follow-up. Now every inquiry gets a call within 5 minutes and I walk into every consultation fully prepared. Three new retainers in the first month alone.",
  },
  {
    image: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7?26",
    name: "Priya K.",
    userName: "Managing Partner, Immigration Law",
    comment:
      "The pre-consultation briefings are game-changing. My RCICs used to spend 30 minutes prepping for each meeting. NeuronX does it automatically. We handle 2x the consultations with the same team.",
  },
  {
    image: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7?11",
    name: "David P.",
    userName: "Intake Coordinator",
    comment:
      "I used to manage leads in spreadsheets and hope I didn't forget anyone. NeuronX's pipeline shows me exactly who to follow up with, when, and why. No lead falls through the cracks.",
  },
  {
    image: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7?5",
    name: "Nina S.",
    userName: "Firm Owner, 8-person Practice",
    comment:
      "We switched from CaseEasy for intake. CaseEasy is great for case management, but NeuronX owns the funnel that feeds us clients. Together they're unbeatable. ROI was clear in week two.",
  },
  {
    image: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7?15",
    name: "Ahmed H.",
    userName: "RCIC, Spousal Sponsorship",
    comment:
      "The AI compliance guardrails give me peace of mind. It never promises outcomes or assesses eligibility. It just collects the right information and books the right people. That's exactly what I need.",
  },
  {
    image: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7?20",
    name: "Sarah L.",
    userName: "Business Development Lead",
    comment:
      "We finally have visibility into our conversion funnel. I can see which programs convert best, which lead sources have the highest ROI, and where prospects get stuck. Data-driven immigration consulting.",
  },
];

export const Testimonials = () => {
  return (
    <section id="testimonials" className="container py-24 sm:py-32">
      <h2 className="text-3xl md:text-4xl font-bold text-center">
        Why Immigration Firms{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          Choose NeuronX
        </span>
      </h2>

      <p className="text-xl text-muted-foreground pt-4 pb-8 text-center">
        From solo practitioners to multi-RCIC firms — NeuronX transforms how
        Canadian immigration consultancies convert and retain clients.
      </p>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 sm:block columns-2 lg:columns-3 lg:gap-6 mx-auto space-y-4 lg:space-y-6">
        {testimonials.map(
          ({ image, name, userName, comment }: TestimonialProps) => (
            <Card
              key={userName}
              className="max-w-md md:break-inside-avoid overflow-hidden"
            >
              <CardHeader className="flex flex-row items-center gap-4 pb-2">
                <Avatar>
                  <AvatarImage alt="" src={image} />
                  <AvatarFallback>
                    {name.split(" ").map((n) => n[0]).join("")}
                  </AvatarFallback>
                </Avatar>

                <div className="flex flex-col">
                  <CardTitle className="text-lg">{name}</CardTitle>
                  <CardDescription>{userName}</CardDescription>
                </div>
              </CardHeader>

              <CardContent>{comment}</CardContent>
            </Card>
          )
        )}
      </div>
    </section>
  );
};
