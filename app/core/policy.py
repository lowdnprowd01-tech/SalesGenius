from dataclasses import dataclass

@dataclass
class Policy:
    dry_run: bool = True
    auto_publish: bool = False
    allow_new_provider_connections: bool = True
    kill_switch: bool = True

    def can_publish(self, provider: str, account_id: str, scopes: list[str]) -> bool:
        allowed = {
            "meta": ["pages_manage_posts", "pages_read_engagement"],
            "shopify": ["write_products", "write_orders"],
            "etsy": ["listings_w"],
            "tiktok": ["video.upload"],
            "youtube": ["https://www.googleapis.com/auth/youtube.upload"],
        }
        if not self.kill_switch:
            return False
        if self.dry_run:
            return False
        if provider not in allowed:
            return False
        required_scopes = allowed[provider]
        return all(scope in scopes for scope in required_scopes)
