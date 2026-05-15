import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import RuntimeGrid from "./components/RuntimeGrid";
import Services from "./components/Services";
import CTA from "./components/CTA";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="bg-[#02040a] text-white min-h-screen overflow-x-hidden">
      <Navbar />
      <Hero />
      <RuntimeGrid />
      <Services />
      <CTA />
      <Footer />
    </div>
  );
}
