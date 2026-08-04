"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useEulaStore } from "@/store/eula-store";
import { useToast } from "@/components/ui/toast";

const EULA_SECTIONS: { title: string; body: string }[] = [
  {
    title: "1. Penggunaan Platform",
    body: "Enal AI OS menyediakan kemampuan AI untuk membantu analisis, eksekusi, dan pengambilan keputusan. Anda setuju untuk menggunakan platform ini sesuai dengan hukum yang berlaku dan tidak menyalahgunakan layanan untuk aktivitas ilegal atau berbahaya.",
  },
  {
    title: "2. Akun dan Keamanan",
    body: "Anda bertanggung jawab menjaga kerahasiaan kredensial akun Anda. Segala aktivitas yang terjadi di bawah akun Anda menjadi tanggung jawab Anda.",
  },
  {
    title: "3. Hasil AI",
    body: "Hasil yang dihasilkan oleh AI bersifat asistif dan tidak menjamin keakuratan absolut. Keputusan akhir tetap berada pada pengguna. Enal AI OS tidak bertanggung jawab atas kerugian yang timbul dari penggunaan hasil AI.",
  },
  {
    title: "4. Data dan Privasi",
    body: "Data yang Anda unggah atau proses melalui platform digunakan untuk menjalankan capability sesuai permintaan Anda. Kami memproses data sesuai dengan kebijakan privasi yang berlaku.",
  },
  {
    title: "5. Batasan Tanggung Jawab",
    body: "Enal AI OS disediakan 'sebagaimana adanya'. Kami tidak memberikan jaminan tersurat maupun tersirat mengenai ketersediaan, keakuratan, atau kesesuaian layanan untuk tujuan tertentu.",
  },
];

export function EulaPage() {
  const router = useRouter();
  const [checked, setChecked] = useState(false);
  const acceptEula = useEulaStore((s) => s.acceptEula);
  const { showError } = useToast();

  const handleContinue = () => {
    if (!checked) {
      showError("Harap centang persetujuan EULA terlebih dahulu.");
      return;
    }
    acceptEula();
    router.push("/dashboard");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--color-bg-primary)] p-4">
      <div className="w-full max-w-2xl space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="text-4xl mb-4">🧠</div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
            Enal AI OS
          </h1>
          <p className="text-sm text-[var(--color-text-secondary)]">
            End User License Agreement
          </p>
        </div>

        {/* EULA content */}
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-6 max-h-[50vh] overflow-y-auto space-y-4">
          <h2 className="text-base font-semibold text-[var(--color-text-primary)]">
            Perjanjian Lisensi Pengguna Akhir
          </h2>
          <p className="text-xs text-[var(--color-text-secondary)]">
            Terakhir diperbarui: versi 1.0.0
          </p>
          <p className="text-sm text-[var(--color-text-primary)] leading-relaxed">
            Dengan menyetujui perjanjian ini, Anda menyatakan telah membaca,
            memahami, dan menyetujui seluruh ketentuan berikut yang mengatur
            penggunaan platform Enal AI OS.
          </p>
          {EULA_SECTIONS.map((section) => (
            <div key={section.title}>
              <h3 className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">
                {section.title}
              </h3>
              <p className="text-xs text-[var(--color-text-secondary)] leading-relaxed">
                {section.body}
              </p>
            </div>
          ))}
        </div>

        {/* Agree checkbox */}
        <label className="flex items-start gap-3 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={checked}
            onChange={(e) => setChecked(e.target.checked)}
            className="mt-0.5 h-4 w-4 rounded border-[var(--color-border)] text-[var(--color-accent)] focus:ring-[var(--color-accent)]"
          />
          <span className="text-sm text-[var(--color-text-primary)]">
            Saya menyetujui EULA dan seluruh ketentuannya
          </span>
        </label>

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={handleContinue}
            disabled={!checked}
            className="flex-1 rounded-lg bg-[var(--color-accent)] px-4 py-2.5 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
          >
            Continue
          </button>
          <button
            onClick={() => router.push("/login")}
            className="rounded-lg border border-[var(--color-border)] px-4 py-2.5 text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
          >
            Sign out
          </button>
        </div>
      </div>
    </div>
  );
}
