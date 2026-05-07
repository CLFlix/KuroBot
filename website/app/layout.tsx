import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "KuroBot",
  description: "A lightweight Twitch bot for osu! streamers!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col text-white font-sans">
        <Header />
        <main className="bg-gradient-to-br from-stone-950 to-neutral-900 flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
