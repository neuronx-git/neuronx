import { Check, X } from "lucide-react";

const rows = [
  { feature: "Structured lead scoring (0-100)", nx: true, crm: false, case_: false },
  { feature: "Pre-consultation briefings", nx: true, crm: false, case_: false },
  { feature: "Trust boundary enforcement", nx: true, crm: false, case_: false },
  { feature: "Immigration-specific workflows", nx: true, crm: false, case_: true },
  { feature: "Inquiry-to-retainer automation", nx: true, crm: false, case_: false },
  { feature: "Case processing pipeline", nx: true, crm: false, case_: true },
  { feature: "Program-specific doc checklists", nx: true, crm: false, case_: true },
  { feature: "IRCC form preparation", nx: true, crm: false, case_: true },
  { feature: "Built-in CRM + pipelines", nx: true, crm: true, case_: false },
  { feature: "Multi-channel follow-up", nx: true, crm: true, case_: false },
];

const Cell = ({ value }: { value: boolean }) => (
  <td className="px-4 py-3 text-center">
    {value ? (
      <Check className="w-5 h-5 text-[#4F46E5] mx-auto" />
    ) : (
      <X className="w-5 h-5 text-slate-300 mx-auto" />
    )}
  </td>
);

export const Differentiation = () => {
  return (
    <section id="compare" className="py-16 sm:py-20">
      <div className="container">
        <div className="text-center mb-16 max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
            How NeuronX{" "}
            <span className="gradient-text">compares</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            NeuronX covers the revenue lifecycle that generic CRMs and
            case-management tools leave untouched.
          </p>
        </div>

        <div className="max-w-4xl mx-auto overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left px-4 py-3 font-medium text-muted-foreground">Capability</th>
                <th className="px-4 py-3 font-bold text-[#4F46E5] text-center">NeuronX</th>
                <th className="px-4 py-3 font-medium text-muted-foreground text-center">Generic CRM</th>
                <th className="px-4 py-3 font-medium text-muted-foreground text-center">Case-First Tools</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.feature} className="border-b border-border hover:bg-muted transition-colors">
                  <td className="px-4 py-3 text-foreground font-medium">{row.feature}</td>
                  <Cell value={row.nx} />
                  <Cell value={row.crm} />
                  <Cell value={row.case_} />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
};
