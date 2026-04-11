import { Building2 } from "lucide-react";

interface SponsorProps {
  icon: JSX.Element;
  name: string;
}

const sponsors: SponsorProps[] = [
  { icon: <Building2 size={34} />, name: "Visa Master Canada" },
  { icon: <Building2 size={34} />, name: "Express Pathways" },
  { icon: <Building2 size={34} />, name: "Northern Immigration" },
  { icon: <Building2 size={34} />, name: "Pacific RCIC Group" },
  { icon: <Building2 size={34} />, name: "Capital Immigration" },
  { icon: <Building2 size={34} />, name: "Atlantic Consulting" },
];

export const Sponsors = () => {
  return (
    <section id="sponsors" className="container pt-24 sm:py-32">
      <h2 className="text-center text-md lg:text-xl font-bold mb-8 text-primary">
        Trusted by Immigration Firms Across Canada
      </h2>

      <div className="flex flex-wrap justify-center items-center gap-4 md:gap-8">
        {sponsors.map(({ icon, name }: SponsorProps) => (
          <div
            key={name}
            className="flex items-center gap-1 text-muted-foreground"
          >
            <span>{icon}</span>
            <h3 className="text-xl font-bold">{name}</h3>
          </div>
        ))}
      </div>
    </section>
  );
};
