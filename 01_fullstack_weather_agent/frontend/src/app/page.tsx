import ChatUI from "@/components/chatUI";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col items-center justify-start px-4 py-10">
      <div className="w-full max-w-3xl">
        <header className="text-center mb-8">
          {/* <h1 className="text-4xl font-bold text-blue-700">Weather Assistant 🌦️</h1> */}
          <p className="text-gray-600 mt-2 text-lg">Ask anything about the weather!</p>
        </header>
        <ChatUI />
      </div>
    </main>
  );
}
