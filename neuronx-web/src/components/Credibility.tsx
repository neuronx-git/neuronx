import { StaggerContainer, StaggerItem } from "./ui/scroll-reveal";
import { Shield, Award, Star, Users, Lock } from "lucide-react";

const credentials = [
  { icon: <Shield className="w-5 h-5" />, label: "RCIC Licensed (R705959)" },
  { icon: <Award className="w-5 h-5" />, label: "CICC Regulated" },
  { icon: <Users className="w-5 h-5" />, label: "5,000+ Clients Served" },
  { icon: <Star className="w-5 h-5" />, label: "5.0 Google Rating" },
  { icon: <Lock className="w-5 h-5" />, label: "PIPEDA Compliant" },
];

export const Credibility = () => {
  return (
    <section className="py-10 border-b border-border">
      <div className="container">
        <StaggerContainer className="flex flex-wrap items-center justify-center gap-8 md:gap-12">
          {credentials.map((c) => (
            <StaggerItem key={c.label}><div
              className="flex items-center gap-2 text-muted-foreground text-sm font-medium"
            >
              <span className="text-[#4F46E5]">{c.icon}</span>
              {c.label}
            </div></StaggerItem>
          ))}
        </StaggerContainer>
      </div>
    </section>
  );
};
