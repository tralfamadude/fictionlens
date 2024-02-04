'use client'
import { usePathname, useRouter } from 'next/navigation';
import Image from 'next/image';

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();

  // Determine button styles based on pathname and focus
  const getButtonStyles = (buttonPath: string) => {
    return {
      background: pathname === buttonPath ? 'black' : 'white',
      color: pathname === buttonPath ? 'white' : 'black',
      border: 'none',
      padding: '10px 20px',
      borderRadius: '5px',
      cursor: 'pointer',
    };
  };

  return (
    <div className="z-10 max-w-5xl w-full flex items-center justify-between font-mono text-sm lg:flex">
      <div className="flex items-center">
        <Image
          src="https://static.vecteezy.com/system/resources/previews/005/393/646/non_2x/lama-flat-style-cute-animal-drawing-for-children-s-textiles-postcards-illustration-vector.jpg"
          alt="logo"
          width={50}
          height={50}
          className="rounded-full"
          loading="lazy"
        />
        <h1 className="text-4xl font-bold ml-2">FictionLens</h1>
      </div>
      <nav>
        <ul className="flex space-x-4">
          <li>
            <button
              onClick={() => router.push('/chat')}
              onFocus={() => { }}
              style={getButtonStyles('/chat')}
            >
              Chat
            </button>
          </li>
          <li>
            <button
              onClick={() => router.push('/story')}
              onFocus={() => { }}
              style={getButtonStyles('/story')}
            >
              Story
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
}
