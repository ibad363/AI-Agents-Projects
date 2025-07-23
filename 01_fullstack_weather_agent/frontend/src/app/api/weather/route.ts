import { NextResponse, NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  const { message } = await req.json()
  const res = await fetch(process.env.BACKEND_URL + '/weather', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ message }),
  })
  const json = await res.json()
  return NextResponse.json({ response: json.response })
}
