from pydantic import BaseModel, validator


class IngestSiteMapIn(BaseModel):
    sitemapUrl: str
    sourceName: str

    @validator("sitemapUrl")
    def sitemap_url_must_be_xml(cls, v):
        if not v.endswith(".xml"):
            raise ValueError("must be a URL to an XML sitemap")
        return v
