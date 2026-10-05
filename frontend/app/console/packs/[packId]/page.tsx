import { PackDetailView } from "@/components/console/packs/pack-detail-view";

export default async function ConsolePackDetailPage({
  params,
}: {
  params: Promise<{ packId: string }>;
}) {
  const { packId } = await params;
  return <PackDetailView packId={decodeURIComponent(packId)} />;
}