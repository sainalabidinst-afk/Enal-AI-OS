import { PackDetailView } from "@/components/console/packs/pack-detail-view";

export default function ConsolePackDetailPage({
  params,
}: {
  params: { packId: string };
}) {
  return <PackDetailView packId={decodeURIComponent(params.packId)} />;
}