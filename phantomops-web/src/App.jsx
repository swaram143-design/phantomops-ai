
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Services from "./components/Services";
import Capabilities from "./components/Capabilities";
import Industries from "./components/Industries";
import Contact from "./components/Contact";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="bg-[#03030a] text-white min-h-screen overflow-x-hidden">
      <Navbar />
      <Hero />
      <Services />
      <Capabilities />
      <Industries />
      <Contact />
      <Footer />
    </div>
  );
}
