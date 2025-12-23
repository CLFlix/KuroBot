"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const Header = () => {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "KuroBot" },
    { href: "/commands", label: "Features" },
    { href: "/about", label: "About" },
  ];

  return (
    <header>
      <nav>
        <ul className="header-gradient text-white text-3xl max-lg:text-xl flex justify-center gap-6 max-lg:gap-5">
          {links.map((link) => (
            <li key={link.href} className="hover:scale-103 duration-300">
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
