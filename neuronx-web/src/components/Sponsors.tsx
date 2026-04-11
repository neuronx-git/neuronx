import { Award, Shield } from "lucide-react";

export const Sponsors = () => {
  return (
    <section id="sponsors" className="container pt-24 sm:py-32">
      <h2 className="text-center text-md lg:text-xl font-bold mb-8 text-primary">
        Built by Immigration Industry Veterans
      </h2>

      <div className="flex flex-wrap justify-center items-center gap-6 md:gap-12">
        <div className="flex items-center gap-2 text-muted-foreground">
          <Shield size={28} />
          <span className="text-lg font-semibold">RCIC Licensed</span>
        </div>
        <div className="flex items-center gap-2 text-muted-foreground">
          <Award size={28} />
          <span className="text-lg font-semibold">CICC Regulated</span>
        </div>
        <div className="flex items-center gap-2 text-muted-foreground">
          <span className="text-lg font-semibold">5,000+ Clients Served</span>
        </div>
        <div className="flex items-center gap-2 text-muted-foreground">
          <span className="text-lg font-semibold">5.0 Google Rating</span>
        </div>
        <div className="flex items-center gap-2 text-muted-foreground">
          <span className="text-lg font-semibold">PIPEDA Compliant</span>
        </div>
      </div>
    </section>
  );
};
