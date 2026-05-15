import { useEffect, useState } from "react";

const API_URL =
  "https://phantomops-ai.onrender.com";

export default function PhantomOpsWebsite() {

  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    need: "",
  });

  const [loading, setLoading] =
    useState(false);

  const [success, setSuccess] =
    useState(false);

  const [adminMode, setAdminMode] =
    useState(false);

  const [leads, setLeads] =
    useState([]);

  const [loadingLeads, setLoadingLeads] =
    useState(false);


  // =====================================
  // SUBMIT LEAD
  // =====================================

  const submitLead = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        `${API_URL}/submit-lead`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify(form),
        }
      );

      const data =
        await response.json();

      console.log(data);

      setSuccess(true);

      setForm({
        name: "",
        email: "",
        company: "",
        need: "",
      });

    } catch (error) {

      console.error(error);
    }

    setLoading(false);
  };


  // =====================================
  // LOAD LEADS
  // =====================================

  const loadLeads = async () => {

    setLoadingLeads(true);

    try {

      const response = await fetch(
        `${API_URL}/leads`
      );

      const data =
        await response.json();

      setLeads(
        data.leads || []
      );

    } catch (error) {

      console.error(error);
    }

    setLoadingLeads(false);
  };


  // =====================================
  // ADMIN SHORTCUT
  // =====================================

  useEffect(() => {

    const handleKeyDown = (e) => {

      if (
        e.ctrlKey
        &&
        e.shiftKey
        &&
        e.key === "A"
      ) {

        setAdminMode(
          (prev) => !prev
        );
      }
    };

    window.addEventListener(
      "keydown",
      handleKeyDown
    );

    return () => {

      window.removeEventListener(
        "keydown",
        handleKeyDown
      );
    };

  }, []);


  useEffect(() => {

    if (adminMode) {

      loadLeads();
    }

  }, [adminMode]);


  // =====================================
  // SERVICES
  // =====================================

  const services = [
    {
      title: "Autonomous AI Operations",
      desc: "Deploy AI systems that monitor, analyze, automate, and optimize business workflows 24/7.",
    },
    {
      title: "Revenue Intelligence",
      desc: "AI-powered lead discovery, CRM intelligence, proposal automation, and predictive analytics.",
    },
    {
      title: "Healthcare AI Automation",
      desc: "Advanced automation infrastructure for clinics, hospitals, diagnostics, and patient workflows.",
    },
  ];


  // =====================================
  // METRICS
  // =====================================

  const metrics = [
    {
      value: "24/7",
      label: "Autonomous Runtime",
    },
    {
      value: "AI",
      label: "Commercial Intelligence",
    },
    {
      value: "CRM",
      label: "Revenue Operations",
    },
    {
      value: "∞",
      label: "Scalable Infrastructure",
    },
  ];


  // =====================================
  // FEATURES
  // =====================================

  const features = [
    "Live Marketplace Intelligence",
    "AI Proposal Generation",
    "Autonomous Followup Systems",
    "Revenue Analytics",
    "AI CRM Infrastructure",
    "Telegram & WhatsApp Automation",
    "Continuous Runtime Systems",
    "Adaptive Learning Intelligence",
  ];


  // =====================================
  // INDUSTRIES
  // =====================================

  const industries = [
    "Healthcare",
    "Hospitals",
    "SaaS",
    "Startups",
    "Agencies",
    "Real Estate",
    "Education",
    "E-Commerce",
  ];


  // =====================================
  // ADMIN CRM DASHBOARD
  // =====================================

  if (adminMode) {

    return (

      <div className="min-h-screen bg-black text-white p-8">

        <div className="max-w-7xl mx-auto">

          <div className="flex items-center justify-between mb-10">

            <div>

              <h1 className="text-5xl font-black">
                PhantomOps CRM
              </h1>

              <p className="text-zinc-400 mt-3">
                Revenue Operations Dashboard
              </p>

            </div>

            <button
              onClick={() =>
                setAdminMode(false)
              }
              className="px-6 py-3 rounded-2xl bg-cyan-500 text-black font-bold"
            >
              Exit Dashboard
            </button>

          </div>


          <div className="grid md:grid-cols-3 gap-6 mb-10">

            <div className="rounded-3xl border border-white/10 bg-white/5 p-8">

              <div className="text-5xl font-black text-cyan-400">
                {leads.length}
              </div>

              <div className="mt-3 text-zinc-400">
                Total Leads
              </div>

            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-8">

              <div className="text-5xl font-black text-emerald-400">
                LIVE
              </div>

              <div className="mt-3 text-zinc-400">
                CRM Runtime
              </div>

            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-8">

              <div className="text-5xl font-black text-purple-400">
                AI
              </div>

              <div className="mt-3 text-zinc-400">
                Automation Active
              </div>

            </div>

          </div>


          <div className="rounded-3xl border border-white/10 overflow-hidden bg-white/5">

            <div className="p-6 border-b border-white/10">

              <h2 className="text-2xl font-bold">
                Lead Pipeline
              </h2>

            </div>

            <div className="overflow-x-auto">

              <table className="w-full">

                <thead className="bg-white/5">

                  <tr>

                    <th className="text-left p-5">
                      Name
                    </th>

                    <th className="text-left p-5">
                      Email
                    </th>

                    <th className="text-left p-5">
                      Company
                    </th>

                    <th className="text-left p-5">
                      Requirement
                    </th>

                    <th className="text-left p-5">
                      Created
                    </th>

                  </tr>

                </thead>

                <tbody>

                  {loadingLeads ? (

                    <tr>

                      <td
                        colSpan="5"
                        className="p-10 text-center text-zinc-400"
                      >
                        Loading CRM...
                      </td>

                    </tr>

                  ) : (

                    leads.map((lead, index) => (

                      <tr
                        key={index}
                        className="border-t border-white/5 hover:bg-white/5"
                      >

                        <td className="p-5">
                          {lead.name}
                        </td>

                        <td className="p-5 text-cyan-400">
                          {lead.email}
                        </td>

                        <td className="p-5">
                          {lead.company}
                        </td>

                        <td className="p-5">
                          {lead.need}
                        </td>

                        <td className="p-5 text-zinc-500">
                          {lead.created_at}
                        </td>

                      </tr>

                    ))

                  )}

                </tbody>

              </table>

            </div>

          </div>

        </div>

      </div>
    );
  }


  // =====================================
  // MAIN WEBSITE
  // =====================================

  return (

    <div className="min-h-screen bg-black text-white overflow-hidden">

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(59,130,246,0.25),transparent_35%)]" />

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_right,rgba(168,85,247,0.2),transparent_30%)]" />

      <div className="relative z-10">

        <nav className="flex items-center justify-between px-8 py-6 lg:px-20 border-b border-white/10 backdrop-blur-md sticky top-0 bg-black/40 z-50">

          <div>

            <h1 className="text-2xl font-black tracking-tight">
              PhantomOps <span className="text-cyan-400">AI</span>
            </h1>

          </div>

          <div className="hidden md:flex items-center gap-8 text-sm text-zinc-300">

            <a href="#services" className="hover:text-white transition">
              Services
            </a>

            <a href="#capabilities" className="hover:text-white transition">
              Capabilities
            </a>

            <a href="#industries" className="hover:text-white transition">
              Industries
            </a>

            <a href="#contact" className="hover:text-white transition">
              Contact
            </a>

          </div>

          <button className="px-5 py-2 rounded-full bg-cyan-500 hover:bg-cyan-400 text-black font-semibold transition">
            Book Consultation
          </button>

        </nav>

        <section className="px-8 py-24 lg:px-20 lg:py-32 max-w-7xl mx-auto">

          <div className="grid lg:grid-cols-2 gap-16 items-center">

            <div>

              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-300 text-sm mb-8">
                Autonomous AI Infrastructure Platform
              </div>

              <h1 className="text-5xl md:text-7xl font-black leading-tight tracking-tight">
                Building
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">
                  AI Business Systems
                </span>
                That Operate 24/7
              </h1>

              <p className="mt-8 text-xl text-zinc-400 leading-relaxed max-w-2xl">
                PhantomOps AI builds autonomous commercial intelligence systems,
                AI workflow automation, CRM infrastructure, revenue analytics,
                and healthcare automation platforms for modern businesses.
              </p>

              <div className="mt-10 flex flex-wrap gap-4">

                <button className="px-8 py-4 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-bold text-lg transition shadow-2xl shadow-cyan-500/20">
                  Start Automation
                </button>

                <button className="px-8 py-4 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 font-semibold text-lg transition">
                  View Demo
                </button>

              </div>

              <div className="mt-12 flex flex-wrap gap-8 text-zinc-400 text-sm">

                <div>
                  <span className="text-white font-bold text-xl">AI</span>
                  <div>Commercial Intelligence</div>
                </div>

                <div>
                  <span className="text-white font-bold text-xl">CRM</span>
                  <div>Revenue Operations</div>
                </div>

                <div>
                  <span className="text-white font-bold text-xl">24/7</span>
                  <div>Autonomous Runtime</div>
                </div>

              </div>

            </div>


            <div className="relative">

              <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-3xl blur-xl opacity-30" />

              <div className="relative bg-zinc-950/80 border border-white/10 rounded-3xl p-8 backdrop-blur-xl shadow-2xl">

                <div className="flex items-center justify-between mb-6">

                  <h3 className="text-xl font-bold">
                    AI Runtime Status
                  </h3>

                  <div className="flex items-center gap-2 text-emerald-400 text-sm">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    LIVE
                  </div>

                </div>


                <div className="space-y-4">

                  {[
                    "Marketplace Intelligence",
                    "CRM Analytics",
                    "Proposal Automation",
                    "Revenue Tracking",
                    "AI Inbox Monitoring",
                    "Autonomous Followups",
                  ].map((item) => (

                    <div
                      key={item}
                      className="flex items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/5"
                    >

                      <span>{item}</span>

                      <span className="text-emerald-400 text-sm">
                        ACTIVE
                      </span>

                    </div>

                  ))}

                </div>


                <div className="mt-8 grid grid-cols-2 gap-4">

                  <div className="p-5 rounded-2xl bg-cyan-500/10 border border-cyan-500/20">

                    <div className="text-4xl font-black text-cyan-400">
                      98%
                    </div>

                    <div className="text-zinc-400 mt-1 text-sm">
                      Automation Efficiency
                    </div>

                  </div>

                  <div className="p-5 rounded-2xl bg-purple-500/10 border border-purple-500/20">

                    <div className="text-4xl font-black text-purple-400">
                      24/7
                    </div>

                    <div className="text-zinc-400 mt-1 text-sm">
                      Autonomous Runtime
                    </div>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </section>


        <section className="px-8 lg:px-20 pb-20">

          <div className="grid md:grid-cols-4 gap-6 max-w-7xl mx-auto">

            {metrics.map((metric) => (

              <div
                key={metric.label}
                className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-lg"
              >

                <div className="text-5xl font-black text-cyan-400">
                  {metric.value}
                </div>

                <div className="mt-3 text-zinc-400">
                  {metric.label}
                </div>

              </div>

            ))}

          </div>

        </section>


        <section
          id="services"
          className="px-8 lg:px-20 py-24 border-t border-white/5"
        >

          <div className="max-w-7xl mx-auto">

            <div className="max-w-3xl mb-16">

              <div className="text-cyan-400 font-semibold mb-4 uppercase tracking-widest text-sm">
                Services
              </div>

              <h2 className="text-4xl md:text-6xl font-black leading-tight">
                Enterprise AI Infrastructure
              </h2>

              <p className="mt-6 text-xl text-zinc-400 leading-relaxed">
                We design and deploy intelligent automation systems that help
                businesses scale operations, automate workflows, and optimize
                revenue pipelines.
              </p>

            </div>


            <div className="grid lg:grid-cols-3 gap-8">

              {services.map((service) => (

                <div
                  key={service.title}
                  className="group rounded-3xl border border-white/10 bg-white/5 p-8 hover:bg-white/10 transition duration-300 backdrop-blur-lg"
                >

                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-r from-cyan-500 to-purple-500 mb-8" />

                  <h3 className="text-2xl font-bold mb-4 group-hover:text-cyan-400 transition">
                    {service.title}
                  </h3>

                  <p className="text-zinc-400 leading-relaxed text-lg">
                    {service.desc}
                  </p>

                </div>

              ))}

            </div>

          </div>

        </section>


        <section
          id="capabilities"
          className="px-8 lg:px-20 py-24 border-t border-white/5"
        >

          <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-20 items-center">

            <div>

              <div className="text-cyan-400 font-semibold mb-4 uppercase tracking-widest text-sm">
                AI Capabilities
              </div>

              <h2 className="text-4xl md:text-6xl font-black leading-tight">
                Autonomous Commercial Intelligence
              </h2>

              <p className="mt-8 text-xl text-zinc-400 leading-relaxed">
                PhantomOps AI combines AI orchestration, analytics,
                automation, CRM intelligence, and continuous runtime systems
                into one scalable infrastructure layer.
              </p>

            </div>


            <div className="grid sm:grid-cols-2 gap-5">

              {features.map((feature) => (

                <div
                  key={feature}
                  className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-lg hover:border-cyan-400/40 transition"
                >

                  <div className="flex items-start gap-4">

                    <div className="w-3 h-3 rounded-full bg-cyan-400 mt-2" />

                    <div className="text-lg text-zinc-200">
                      {feature}
                    </div>

                  </div>

                </div>

              ))}

            </div>

          </div>

        </section>


        <section
          id="industries"
          className="px-8 lg:px-20 py-24 border-t border-white/5"
        >

          <div className="max-w-7xl mx-auto">

            <div className="text-cyan-400 font-semibold mb-4 uppercase tracking-widest text-sm">
              Industries
            </div>

            <h2 className="text-4xl md:text-6xl font-black leading-tight max-w-4xl">
              Built For High-Impact Industries
            </h2>

            <div className="mt-16 flex flex-wrap gap-5">

              {industries.map((industry) => (

                <div
                  key={industry}
                  className="px-8 py-4 rounded-full bg-white/5 border border-white/10 text-lg hover:bg-cyan-500 hover:text-black transition font-medium"
                >
                  {industry}
                </div>

              ))}

            </div>

          </div>

        </section>


        <section
          id="contact"
          className="px-8 lg:px-20 py-24 border-t border-white/5"
        >

          <div className="max-w-6xl mx-auto rounded-[40px] border border-white/10 bg-gradient-to-br from-cyan-500/10 to-purple-500/10 p-10 md:p-16 backdrop-blur-xl">

            <div className="grid lg:grid-cols-2 gap-16 items-center">

              <div>

                <div className="text-cyan-400 font-semibold mb-4 uppercase tracking-widest text-sm">
                  Start Building
                </div>

                <h2 className="text-4xl md:text-6xl font-black leading-tight">
                  Build Your AI Infrastructure
                </h2>

                <p className="mt-8 text-xl text-zinc-300 leading-relaxed">
                  Deploy autonomous AI systems that automate workflows,
                  optimize revenue operations, and scale business intelligence.
                </p>

              </div>


              <div className="space-y-5">

                <input
                  placeholder="Your Name"
                  value={form.name}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      name: e.target.value,
                    })
                  }
                  className="w-full px-6 py-5 rounded-2xl bg-black/40 border border-white/10 outline-none focus:border-cyan-400 text-lg"
                />

                <input
                  placeholder="Email Address"
                  value={form.email}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      email: e.target.value,
                    })
                  }
                  className="w-full px-6 py-5 rounded-2xl bg-black/40 border border-white/10 outline-none focus:border-cyan-400 text-lg"
                />

                <input
                  placeholder="Company"
                  value={form.company}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      company: e.target.value,
                    })
                  }
                  className="w-full px-6 py-5 rounded-2xl bg-black/40 border border-white/10 outline-none focus:border-cyan-400 text-lg"
                />

                <textarea
                  placeholder="What would you like to automate?"
                  rows={5}
                  value={form.need}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      need: e.target.value,
                    })
                  }
                  className="w-full px-6 py-5 rounded-2xl bg-black/40 border border-white/10 outline-none focus:border-cyan-400 text-lg"
                />

                <button
                  onClick={submitLead}
                  className="w-full py-5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black text-xl font-black transition shadow-2xl shadow-cyan-500/20"
                >
                  {loading ? "Submitting..." : "Request Consultation"}
                </button>

                {success && (

                  <div className="text-emerald-400 text-lg font-semibold">
                    Lead submitted successfully.
                  </div>

                )}

              </div>

            </div>

          </div>

        </section>


        <footer className="px-8 lg:px-20 py-12 border-t border-white/5">

          <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">

            <div>

              <h3 className="text-2xl font-black">
                PhantomOps <span className="text-cyan-400">AI</span>
              </h3>

              <p className="text-zinc-500 mt-2">
                Autonomous AI Operations Infrastructure
              </p>

            </div>

            <div className="text-zinc-500 text-sm">
              © 2026 PhantomOps AI. All rights reserved.
            </div>

          </div>

        </footer>

      </div>

    </div>
  );
}
