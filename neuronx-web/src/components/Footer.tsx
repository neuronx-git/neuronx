export const Footer = () => {
  return (
    <footer id="footer">
      <hr className="w-11/12 mx-auto" />

      <section className="container py-20 grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-x-12 gap-y-8">
        <div className="col-span-full xl:col-span-2">
          <a href="/" className="flex items-center gap-2">
            <img src="/logo-light.png" alt="NeuronX" className="h-9 dark:hidden" style={{ background: 'transparent' }} />
            <img src="/logo-dark.png" alt="NeuronX" className="h-9 hidden dark:block" style={{ background: 'transparent' }} />
            <div className="flex flex-col">
              <span className="text-lg font-bold tracking-tight leading-none">NeuronX</span>
              <span className="text-[10px] text-muted-foreground font-normal leading-tight">
                Revenue & Operations System
                <br />
                for Canadian Immigration Firms
              </span>
            </div>
          </a>
        </div>

        <div className="flex flex-col gap-2">
          <h3 className="font-bold text-lg">Product</h3>
          <a href="#features" className="opacity-60 hover:opacity-100">Features</a>
          <a href="#pricing" className="opacity-60 hover:opacity-100">Pricing</a>
          <a href="#howItWorks" className="opacity-60 hover:opacity-100">How It Works</a>
          <a href="#faq" className="opacity-60 hover:opacity-100">FAQ</a>
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
          <a href="#team" className="opacity-60 hover:opacity-100">About</a>
          <a href="mailto:hello@neuronx.co" className="opacity-60 hover:opacity-100">Contact</a>
          <span className="opacity-60">Privacy Policy</span>
          <span className="opacity-60">Terms of Service</span>
        </div>

        <div className="flex flex-col gap-2">
          <h3 className="font-bold text-lg">Connect</h3>
          <a href="https://www.linkedin.com/company/neuronx" target="_blank" rel="noreferrer noopener" className="opacity-60 hover:opacity-100">LinkedIn</a>
          <a href="mailto:hello@neuronx.co" className="opacity-60 hover:opacity-100">Email</a>
        </div>
      </section>

      <section className="container pb-14 text-center">
        <h3>
          &copy; 2026 NeuronX. All rights reserved.
          <span className="text-muted-foreground text-sm ml-2">
            NeuronX is not a law firm and does not provide immigration advice.
          </span>
        </h3>
      </section>
    </footer>
  );
};
