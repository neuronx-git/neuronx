import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import {
  Inbox,
  BarChart3,
  Filter,
  Calendar,
  FileText,
  FolderOpen,
  ClipboardCheck,
  FileSpreadsheet,
  GitBranch,
  CheckCircle,
} from "lucide-react";

const phase1Items = [
  { icon: <Inbox className="w-5 h-5" />, label: "Inquiry capture" },
  { icon: <BarChart3 className="w-5 h-5" />, label: "Structured readiness scoring" },
  { icon: <Filter className="w-5 h-5" />, label: "Qualification and routing" },
  { icon: <Calendar className="w-5 h-5" />, label: "Consultation booking" },
  { icon: <FileText className="w-5 h-5" />, label: "Auto-generated briefings" },
];

const phase2Items = [
  { icon: <FolderOpen className="w-5 h-5" />, label: "10-stage case pipeline" },
  { icon: <ClipboardCheck className="w-5 h-5" />, label: "Program-specific document checklists" },
  { icon: <FileSpreadsheet className="w-5 h-5" />, label: "IRCC form preparation support" },
  { icon: <GitBranch className="w-5 h-5" />, label: "Workflow-driven follow-up" },
  { icon: <CheckCircle className="w-5 h-5" />, label: "Stage tracking through decision" },
];

export const TwoPhase = () => {
  return (
    <section id="system" className="bg-[#1E293B] text-white py-16 sm:py-20">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
            From inquiry to case decision —{" "}
            <span className="gradient-text">structured, scored, and managed.</span>
          </h2>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Phase 1 */}
          <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:border-[#4F46E5]/40 transition-all duration-300">
            <CardHeader>
              <Badge className="w-fit bg-[#4F46E5]/20 text-[#818CF8] border-0 mb-3">
                Phase 1
              </Badge>
              <CardTitle className="text-xl text-white">
                Convert more of the right inquiries
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {phase1Items.map((item) => (
                <div key={item.label} className="flex items-center gap-3">
                  <div className="text-[#818CF8]">{item.icon}</div>
                  <span className="text-slate-300 text-sm">{item.label}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Phase 2 */}
          <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:border-[#7C3AED]/40 transition-all duration-300">
            <CardHeader>
              <Badge className="w-fit bg-[#7C3AED]/20 text-[#A78BFA] border-0 mb-3">
                Phase 2
              </Badge>
              <CardTitle className="text-xl text-white">
                Run case operations with more structure
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {phase2Items.map((item) => (
                <div key={item.label} className="flex items-center gap-3">
                  <div className="text-[#A78BFA]">{item.icon}</div>
                  <span className="text-slate-300 text-sm">{item.label}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Score Card Preview — spans full width under both phase cards */}
        <div className="mt-12 max-w-5xl mx-auto">
          <Card className="bg-white/5 border-white/10 backdrop-blur-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-white font-semibold">Readiness Score</span>
              <span className="text-3xl font-bold text-[#4F46E5]">87<span className="text-lg text-slate-400">/100</span></span>
            </div>
            <div className="space-y-2">
              {[
                { label: "R1 — Program Interest", value: 95 },
                { label: "R2 — Current Location", value: 90 },
                { label: "R3 — Timeline Urgency", value: 80 },
                { label: "R4 — Prior Applications", value: 85 },
                { label: "R5 — Budget Awareness", value: 88 },
              ].map((dim) => (
                <div key={dim.label} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">{dim.label}</span>
                    <span className="text-slate-300">{dim.value}%</span>
                  </div>
                  <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-[#4F46E5] to-[#7C3AED] rounded-full transition-all duration-1000"
                      style={{ width: `${dim.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 flex items-center gap-2">
              <Badge className="bg-emerald-500/20 text-emerald-400 border-0 text-xs">
                Ready — Standard
              </Badge>
              <span className="text-xs text-slate-500">Express Entry</span>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};
