import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Check } from "lucide-react";

enum PopularPlanType {
  NO = 0,
  YES = 1,
}

interface PricingProps {
  title: string;
  popular: PopularPlanType;
  price: number;
  description: string;
  buttonText: string;
  benefitList: string[];
}

const pricingList: PricingProps[] = [
  {
    title: "Essentials",
    popular: 0,
    price: 299,
    description: "For firms starting with AI-powered intake automation.",
    buttonText: "Start Free Trial",
    benefitList: [
      "AI voice intake (100 calls/mo)",
      "Lead readiness scoring (R1-R5)",
      "1 pipeline with 10 stages",
      "Automated booking + reminders",
      "No-show recovery workflow",
      "Email + SMS sequences",
    ],
  },
  {
    title: "Professional",
    popular: 1,
    price: 599,
    description: "For growing firms that want full funnel automation.",
    buttonText: "Start Free Trial",
    benefitList: [
      "Everything in Essentials",
      "Unlimited AI calls",
      "Pre-consultation briefings",
      "9-branch program nurture",
      "IRCC form data sheets",
      "Chrome extension (auto-fill)",
      "Advanced analytics",
      "Case processing pipeline",
    ],
  },
  {
    title: "Scale",
    popular: 0,
    price: 1199,
    description: "For multi-RCIC firms and high-volume practices.",
    buttonText: "Contact Sales",
    benefitList: [
      "Everything in Professional",
      "Multi-RCIC round-robin",
      "E-signatures",
      "Custom client portal",
      "Commission tracking",
      "Dedicated success manager",
    ],
  },
];

export const Pricing = () => {
  return (
    <section id="pricing" className="container py-24 sm:py-32">
      <h2 className="text-3xl md:text-4xl font-bold text-center">
        Simple, Per-Firm
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          {" "}Pricing{" "}
        </span>
      </h2>
      <h3 className="text-xl text-center text-muted-foreground pt-4 pb-8">
        No per-seat fees. One retained client ($3K-$5K) pays for 6+ months of
        NeuronX. All plans include 14-day free trial.
      </h3>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {pricingList.map((pricing: PricingProps) => (
          <Card
            key={pricing.title}
            className={
              pricing.popular === PopularPlanType.YES
                ? "drop-shadow-xl shadow-black/10 dark:shadow-white/10"
                : ""
            }
          >
            <CardHeader>
              <CardTitle className="flex item-center justify-between">
                {pricing.title}
                {pricing.popular === PopularPlanType.YES ? (
                  <Badge variant="secondary" className="text-sm text-primary">Most popular</Badge>
                ) : null}
              </CardTitle>
              <div>
                <span className="text-3xl font-bold">${pricing.price}</span>
                <span className="text-muted-foreground"> /month CAD</span>
              </div>
              <CardDescription>{pricing.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <a href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW" target="_blank" rel="noreferrer noopener">
                <Button className="w-full">{pricing.buttonText}</Button>
              </a>
            </CardContent>
            <hr className="w-4/5 m-auto mb-4" />
            <CardFooter className="flex">
              <div className="space-y-4">
                {pricing.benefitList.map((benefit: string) => (
                  <span key={benefit} className="flex">
                    <Check className="text-green-500" /> <h3 className="ml-2">{benefit}</h3>
                  </span>
                ))}
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>
    </section>
  );
};
