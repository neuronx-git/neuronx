import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "NeuronX — AI Sales OS for Immigration Firms",
    template: "%s | NeuronX",
  },
  description:
    "Convert every immigration inquiry into a retained client. AI-powered intake, scoring, booking, and consultation prep — built for Canadian RCIC firms.",
  metadataBase: new URL("https://neuronx.co"),
  openGraph: {
    type: "website",
    locale: "en_CA",
    siteName: "NeuronX",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} antialiased`}>
      <body className="min-h-screen bg-[#FFFBF5] text-slate-900 font-sans">
        {children}
      </body>
    </html>
  );
}
