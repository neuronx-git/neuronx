import { buttonVariants } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Linkedin } from "lucide-react";

interface TeamProps {
  imageUrl: string;
  name: string;
  position: string;
  description: string;
  socialNetworks: SociaNetworkslProps[];
}

interface SociaNetworkslProps {
  name: string;
  url: string;
}

const teamList: TeamProps[] = [
  {
    imageUrl: "/team/ranjan.jpg",
    name: "Ranjan Singh",
    position: "Co-Founder & CEO",
    description:
      "Former Big Five consulting leader with deep expertise in product management, sales operations, and technology transformation. Built and scaled enterprise software products used by Fortune 500 companies. Now applying that discipline to immigration consulting — because every firm deserves enterprise-grade tools without the enterprise price tag.",
    socialNetworks: [
      { name: "Linkedin", url: "https://www.linkedin.com/in/ranjansingh/" },
    ],
  },
  {
    imageUrl: "/team/sanjay.jpg",
    name: "Sanjay Singh Kumar",
    position: "Co-Founder & Chief Immigration Officer",
    description:
      "Licensed RCIC (R705959) and founder of Visa Master Canada — a 20-person immigration firm with 5,000+ clients served and a perfect 5.0 Google rating. Seven years of hands-on immigration consulting across Express Entry, LMIA, Spousal Sponsorship, and complex refusal cases. The domain expert who ensures every NeuronX feature solves a real problem that RCICs face daily.",
    socialNetworks: [
      { name: "Linkedin", url: "https://www.linkedin.com/in/sanjaysinghkumar/" },
    ],
  },
];

export const Team = () => {
  const socialIcon = (iconName: string) => {
    switch (iconName) {
      case "Linkedin":
        return <Linkedin size="20" />;
    }
  };

  return (
    <section id="team" className="container py-24 sm:py-32">
      <h2 className="text-3xl md:text-4xl font-bold text-center">
        Built by{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          Two Brothers
        </span>{" "}
        Who Know the Problem
      </h2>

      <p className="mt-4 mb-10 text-xl text-muted-foreground text-center max-w-3xl mx-auto">
        NeuronX was born when a Big Five consulting veteran saw his RCIC brother
        losing clients to slow follow-up and unprepared consultations. Together,
        they built the system that every immigration firm needs but nobody had
        created — an AI sales OS designed by practitioners, for practitioners.
      </p>

      <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8 gap-y-10 max-w-4xl mx-auto">
        {teamList.map(
          ({
            imageUrl,
            name,
            position,
            description,
            socialNetworks,
          }: TeamProps) => (
            <Card
              key={name}
              className="bg-muted/50 relative mt-8 flex flex-col justify-center items-center"
            >
              <CardHeader className="mt-8 flex justify-center items-center pb-2">
                <img
                  src={imageUrl}
                  alt={`${name} ${position}`}
                  className="absolute -top-12 rounded-full w-24 h-24 aspect-square object-cover"
                />
                <CardTitle className="text-center">{name}</CardTitle>
                <CardDescription className="font-normal text-primary">
                  {position}
                </CardDescription>
              </CardHeader>

              <CardContent className="text-center pb-2">
                <p>{description}</p>
              </CardContent>

              <CardFooter>
                {socialNetworks.map(({ name, url }: SociaNetworkslProps) => (
                  <div key={name}>
                    <a
                      rel="noreferrer noopener"
                      href={url}
                      target="_blank"
                      className={buttonVariants({
                        variant: "ghost",
                        size: "sm",
                      })}
                    >
                      <span className="sr-only">{name} icon</span>
                      {socialIcon(name)}
                    </a>
                  </div>
                ))}
              </CardFooter>
            </Card>
          )
        )}
      </div>
    </section>
  );
};
