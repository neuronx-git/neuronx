export const Footer = () => {
  return (
    <footer id="footer">
      <hr className="w-11/12 mx-auto" />

      <section className="container py-16 md:py-20 grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-x-8 md:gap-x-12 gap-y-8">
        <div className="col-span-full xl:col-span-2">
          <a href="/" className="flex items-center gap-2.5">
            <img src="/logo-transparent.svg" alt="NeuronX" className="h-8 dark:hidden" />
            <img src="/logo-dark.svg" alt="NeuronX" className="h-8 hidden dark:block" />
          </a>
          <p className="mt-3 text-[11px] font-bold leading-tight tracking-wide bg-gradient-to-r from-[#4F46E5] to-[#7C3AED] bg-clip-text text-transparent inline-block">
            Revenue & Operations System<br />for Canadian Immigration Firms
          </p>
        </div>

        <div className="flex flex-col gap-2">
          <h3 className="font-bold text-lg">Product</h3>
          <a href="#features" className="opacity-60 hover:opacity-100 transition-opacity">Features</a>
          <a href="#pricing" className="opacity-60 hover:opacity-100 transition-opacity">Pricing</a>
          <a href="#howItWorks" className="opacity-60 hover:opacity-100 transition-opacity">How It Works</a>
          <a href="#faq" className="opacity-60 hover:opacity-100 transition-opacity">FAQ</a>
        </div>

        <div className="flex flex-col gap-2">
          <h3 className="font-bold text-lg">Programs</h3>
          <span className="opacity-60">Express Entry</span>
          <span className="opacity-60">Spousal Sponsorship</span>
          <span className="opacity-60">Work Permit</span>
          <span className="opacity-60">Study Permit</span>
        </div>

        <div className="flex flex-col gap-2">
          <h3 className="font-bold text-lg">Company</h3>
          <a href="#team" className="opacity-60 hover:opacity-100 transition-opacity">About</a>
          <a href="mailto:hello@neuronx.co" className="opacity-60 hover:opacity-100 transition-opacity">Contact</a>
          <a href="/privacy" className="opacity-60 hover:opacity-100 transition-opacity">Privacy Policy</a>
          <a href="/terms" className="opacity-60 hover:opacity-100 transition-opacity">Terms of Service</a>
        </div>

        <div className="flex flex-col gap-2">
          <h3 className="font-bold text-lg">Connect</h3>
          <a href="https://www.linkedin.com/company/neuronx" target="_blank" rel="noreferrer noopener" className="opacity-60 hover:opacity-100 transition-opacity">LinkedIn</a>
          <a href="mailto:hello@neuronx.co" className="opacity-60 hover:opacity-100 transition-opacity">Email</a>
        </div>
      </section>

      <section className="container pb-14 text-center">
        <p className="text-sm text-muted-foreground">
          &copy; 2026 NeuronX. All rights reserved.
          <span className="ml-2 text-xs">
            NeuronX is not a law firm and does not provide immigration advice.
          </span>
        </p>
      </section>
    </footer>
  );
};
