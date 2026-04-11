import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { Badge } from "./ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Check } from "lucide-react";
import { LightBulbIcon } from "./Icons";

export const HeroCards = () => {
  return (
    <div className="hidden lg:flex flex-row flex-wrap gap-8 relative w-[700px] h-[550px]">
      {/* Live metric card */}
      <Card className="absolute w-[340px] -top-[15px] drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader className="flex flex-row items-center gap-4 pb-2">
          <Avatar>
            <AvatarImage alt="" src="https://i.pravatar.cc/150?img=32" />
            <AvatarFallback>RS</AvatarFallback>
          </Avatar>
          <div className="flex flex-col">
            <CardTitle className="text-lg">Rajiv Sharma, RCIC</CardTitle>
            <CardDescription>Express Entry Specialist</CardDescription>
          </div>
        </CardHeader>
        <CardContent>
          "NeuronX calls my prospects before I even finish my morning coffee.
          Three new retainers last month — all from AI-qualified leads."
        </CardContent>
      </Card>

      {/* Speed metric */}
      <Card className="absolute right-[20px] top-4 w-80 flex flex-col justify-center items-center drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader className="mt-8 flex justify-center items-center pb-2">
          <div className="absolute -top-12 rounded-full w-24 h-24 bg-gradient-to-br from-[#E8380D] to-[#F59E0B] flex items-center justify-center">
            <span className="text-white text-2xl font-bold">&lt;5m</span>
          </div>
          <CardTitle className="text-center">Speed to First Contact</CardTitle>
          <CardDescription className="font-normal text-primary">
            AI calls every inquiry within 5 minutes
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center pb-2">
          <p>
            While your competitors take 24+ hours to respond, NeuronX ensures
            every prospect gets a professional follow-up call in minutes.
          </p>
        </CardContent>
      </Card>

      {/* ROI card */}
      <Card className="absolute top-[220px] left-[30px] w-72 drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader>
          <CardTitle className="flex item-center justify-between">
            ROI Calculator
            <Badge variant="secondary" className="text-sm text-primary">
              Proven
            </Badge>
          </CardTitle>
          <div>
            <span className="text-3xl font-bold">1 Client</span>
            <span className="text-muted-foreground"> = 6 months</span>
          </div>
          <CardDescription>
            One retained client ($3K-$5K) pays for 6+ months of NeuronX.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <a href="#pricing">
            <Button className="w-full">See Pricing &amp; ROI</Button>
          </a>
        </CardContent>

        <hr className="w-4/5 m-auto mb-4" />

        <CardFooter className="flex">
          <div className="space-y-4">
            {[
              "3x faster lead response",
              "90% assessment completion",
              "2x consultation show rate",
            ].map((benefit: string) => (
              <span key={benefit} className="flex">
                <Check className="text-green-500" />
                <h3 className="ml-2">{benefit}</h3>
              </span>
            ))}
          </div>
        </CardFooter>
      </Card>

      {/* Compliance card */}
      <Card className="absolute w-[350px] -right-[10px] bottom-[35px] drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader className="space-y-1 flex md:flex-row justify-start items-start gap-4">
          <div className="mt-1 bg-primary/20 p-1 rounded-2xl">
            <LightBulbIcon />
          </div>
          <div>
            <CardTitle>RCIC Compliance Built In</CardTitle>
            <CardDescription className="text-md mt-2">
              Trust boundaries enforced in every AI interaction. The AI never
              assesses eligibility or interprets immigration law.
            </CardDescription>
          </div>
        </CardHeader>
      </Card>
    </div>
  );
};
