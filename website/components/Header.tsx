import Link from "next/link";

const Header = () => {
  return (
    <header>
      <nav>
        <ul className="bg-black flex flex-row gap-5 text-2xl font-sans p-px justify-center list-none">
          <Link href="/">Home</Link>
          <Link href="/commands">Commands</Link>
          <Link href="/about">About</Link>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
