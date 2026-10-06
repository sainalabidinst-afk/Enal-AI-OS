import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PUBLIC_PATHS = ['/login'];
const PROTECTED_PATHS = [
  '/dashboard',
  '/trading',
  '/capability-packs',
  '/builder',
  '/evaluation',
  '/benchmark',
  '/marketplace',
  '/voice',
  '/settings',
  '/observability',
  '/governance',
  '/audit-trail',
  '/search',
];

function getAccessToken(request: NextRequest): string | null {
  return request.cookies.get('access_token')?.value ?? null;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = getAccessToken(request);
  const isPublic = PUBLIC_PATHS.some((path) => pathname === path || pathname.startsWith(path + '/'));
  const isProtected = PROTECTED_PATHS.some((path) => pathname === path || pathname.startsWith(path + '/'));

  if (isPublic) {
    if (token && pathname === '/login') {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
    return NextResponse.next();
  }

  if (isProtected) {
    if (!token) {
      const loginUrl = new URL('/login', request.url);
      loginUrl.searchParams.set('next', pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};

