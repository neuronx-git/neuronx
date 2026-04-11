import { Card, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { MagnifierIcon, WalletIcon, ChartIcon } from "./Icons";

interface ServiceProps {
  title: string;
  description: string;
  icon: JSX.Element;
}

const serviceList: ServiceProps[] = [
  {
    title: "Phase 1: Lead Conversion",
    description:
      "AI-powered intake calling, structured readiness scoring, automated booking, and pre-consultation briefings. Convert more inquiries into paying clients with zero manual follow-up.",
    icon: <ChartIcon />,
  },
  {
    title: "Phase 2: Case Processing",
    description:
      "9-stage case pipeline from onboarding to decision. Document collection workflows, IRCC form data sheets, and real-time case status tracking for your entire caseload.",
    icon: <WalletIcon />,
  },
  {
    title: "GHL-Powered, Not GHL-Limited",
    description:
      "NeuronX runs on GoHighLevel — the same CRM you might already use. But it adds what GHL can't do alone: AI calling, immigration-specific scoring, compliance enforcement, and RCIC briefings.",
    icon: <MagnifierIcon />,
  },
];

export const Services = () => {
  return (
    <section className="container py-24 sm:py-32">
      <div className="grid lg:grid-cols-[1fr,1fr] gap-8 place-items-center">
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

          <div className="flex flex-col gap-8">
            {serviceList.map(({ icon, title, description }: ServiceProps) => (
              <Card key={title}>
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
              </Card>
            ))}
          </div>
        </div>

        <div className="bg-gradient-to-br from-[#0F172A] to-[#1E293B] rounded-2xl p-12 w-full max-w-md aspect-square flex flex-col items-center justify-center text-center">
          <div className="text-6xl font-extrabold text-[#E8380D] mb-4">24</div>
          <div className="text-white text-xl font-semibold mb-2">Automated Workflows</div>
          <div className="text-slate-400 text-sm">
            15 intake + 9 case processing workflows — all running 24/7 so your
            team never has to chase a lead or miss a deadline.
          </div>
        </div>
      </div>
    </section>
  );
};
