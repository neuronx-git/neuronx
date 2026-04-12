import { Card, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { MagnifierIcon, WalletIcon, ChartIcon } from "./Icons";
import { ScrollReveal, StaggerContainer, StaggerItem } from "./ui/scroll-reveal";

interface ServiceProps {
  title: string;
  description: string;
  icon: JSX.Element;
}

const serviceList: ServiceProps[] = [
  {
    title: "Phase 1: Lead Conversion",
    description:
      "Structured readiness scoring, automated booking, and auto-generated pre-consultation briefings. Convert more inquiries into paying clients with structured follow-up workflows.",
    icon: <ChartIcon />,
  },
  {
    title: "Phase 2: Case Processing",
    description:
      "10-stage case pipeline from onboarding to decision. Document collection workflows, IRCC form data sheets, and stage-based case tracking for your entire caseload.",
    icon: <WalletIcon />,
  },
  {
    title: "Built-In CRM + AI Intelligence",
    description:
      "NeuronX includes a fully integrated CRM with contacts, pipelines, email, SMS, and workflows. On top of that, it adds what generic CRMs cannot: AI calling, immigration-specific scoring, compliance enforcement, and RCIC briefings.",
    icon: <MagnifierIcon />,
  },
];

export const Services = () => {
  return (
    <section className="container py-14 sm:py-16">
      <div className="grid lg:grid-cols-[1fr,1fr] gap-8 place-items-center">
        <ScrollReveal>
        <div>
          <h2 className="text-3xl md:text-4xl font-bold">
            <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
              Two Phases.{" "}
            </span>
            One System.
          </h2>

          <p className="text-muted-foreground text-xl mt-4 mb-8 ">
            Most immigration software handles case management AFTER the client
            signs. NeuronX handles everything BEFORE — from first inquiry to
            signed retainer — then seamlessly transitions to case processing.
          </p>

          <StaggerContainer className="flex flex-col gap-8">
            {serviceList.map(({ icon, title, description }: ServiceProps) => (
              <StaggerItem key={title}><Card className="card-premium hover:-translate-y-1 hover:scale-[1.01] transition-all duration-300">
                <CardHeader className="space-y-1 flex md:flex-row justify-start items-start gap-4">
                  <div className="mt-1 bg-primary/20 p-1 rounded-2xl">
                    {icon}
                  </div>
                  <div>
                    <CardTitle>{title}</CardTitle>
                    <CardDescription className="text-md mt-2">
                      {description}
                    </CardDescription>
                  </div>
                </CardHeader>
              </Card></StaggerItem>
            ))}
          </StaggerContainer>
        </div>
        </ScrollReveal>

        <div className="bg-gradient-to-br from-[#0F172A] to-[#1E293B] rounded-2xl p-12 w-full max-w-md aspect-square flex flex-col items-center justify-center text-center">
          <div className="text-6xl font-extrabold text-[#4F46E5] mb-4">13</div>
          <div className="text-white text-xl font-semibold mb-2">Published Workflows</div>
          <div className="text-slate-400 text-sm">
            Immigration-specific workflows covering intake, scoring, booking,
            follow-up, nurture, and case transitions — running so your team
            never has to chase a lead or miss a deadline.
          </div>
        </div>
      </div>
    </section>
  );
};
