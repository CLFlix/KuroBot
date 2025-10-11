"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const Header = () => {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "KuroBot" },
    { href: "/commands", label: "Commands" },
    { href: "/about", label: "About" },
  ];

  return (
    <header>
      <nav>
        <ul className="bg-purple-600 text-white text-3xl font-sans flex justify-center gap-6">
          {links.map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                className={pathname === link.href ? "font-bold" : ""}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
