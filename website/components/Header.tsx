import Link from "next/link";

const Header = () => {
  return (
    <header>
      <nav>
        <ul className="bg-purple-600 text-white text-3xl font-sans flex justify-center gap-6">
          <Link href="/">Home</Link>
          <Link href="/commands">Commands</Link>
          <Link href="/about">About</Link>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
