export function SocialProof() {
  return (
    <section className="py-12 px-6 bg-[#FFFBF5] border-b border-black/5">
      <div className="max-w-6xl mx-auto">
        <p className="text-center text-sm text-slate-500 mb-8">
          Trusted by immigration consulting firms across Canada
        </p>
        <div className="flex flex-wrap items-center justify-center gap-12 opacity-40">
          {["Visa Master Canada", "Express Pathways", "Northern Immigration", "Pacific RCIC Group", "Capital Immigration"].map(
            (name) => (
              <div key={name} className="text-base font-semibold text-slate-900 tracking-tight">
                {name}
              </div>
            )
          )}
        </div>
      </div>
    </section>
  );
}
