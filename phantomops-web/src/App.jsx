import { useState } from "react";

export default function App() {

  const [crm, setCrm] = useState(false);

  return (

    <div className="min-h-screen bg-black text-white p-10">

      {

        crm ? (

          <div>

            <div className="flex justify-between items-center mb-10">

              <h1 className="text-5xl font-black text-cyan-400">
                PhantomOps CRM
              </h1>

              <button
                onClick={() => setCrm(false)}
                className="px-5 py-3 bg-red-500 rounded-xl"
              >
                Exit Dashboard
              </button>

            </div>

            <div className="bg-white/5 p-10 rounded-3xl border border-white/10">

              <h2 className="text-3xl font-bold mb-6">
                CRM Runtime Active
              </h2>

              <p className="text-zinc-400">
                Stable frontend rebuild successful.
              </p>

            </div>

          </div>

        ) : (

          <div className="text-center pt-32">

            <h1 className="text-7xl font-black">

              PhantomOps

              <span className="text-cyan-400">
                {" "}AI
              </span>

            </h1>

            <p className="text-zinc-400 mt-8 text-xl">

              Revenue Automation Infrastructure

            </p>

            <div className="mt-12 flex gap-4 justify-center">

              <button
                onClick={() => setCrm(true)}
                className="px-8 py-4 bg-purple-500 rounded-2xl text-white font-bold"
              >
                Open CRM
              </button>

              <a
                href="#"
                className="px-8 py-4 bg-cyan-500 rounded-2xl text-black font-bold"
              >
                Start Automation
              </a>

            </div>

          </div>

        )

      }

    </div>

  );
}
