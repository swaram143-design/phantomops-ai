export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-black px-6 py-10">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-5">

        <div>
          <h2 className="text-3xl font-black text-cyan-400">
            PhantomOps AI
          </h2>

          <p className="text-zinc-500 text-sm mt-2">
            Autonomous AI Infrastructure Platform
          </p>
        </div>

        <p className="text-zinc-600 text-sm">
          © 2026 PhantomOps AI — All Rights Reserved
        </p>

      </div>
    </footer>
  );
}
