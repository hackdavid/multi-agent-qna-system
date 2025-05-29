OrganizationSchema = [
  {
    "name": "organization_id",
    "description": "Unique identifier for the organization in the system.",
    "label": "Organization ID",
    "format": "str"
  },
  {
    "name": "company_name",
    "description": "Official legal name of the company.",
    "label": "Company Name",
    "format": "str"
  },
  {
    "name": "domain_url",
    "description": "Official domain URL of the company.",
    "label": "Domain URL",
    "format": "str"
  },
  {
    "name": "headquarters_country",
    "description": "Country of the company’s global headquarters.",
    "label": "Headquarters Country",
    "format": "str"
  },
  {
    "name": "headquarters_state",
    "description": "State or region of the company’s headquarters.",
    "label": "Headquarters State",
    "format": "str"
  },
  {
    "name": "headquarters_city",
    "description": "City where the company is headquartered.",
    "label": "Headquarters City",
    "format": "str"
  },
  {
    "name": "customer_stage_archetype",
    "description": "Confirmed business model and stage of the company.",
    "label": "Customer Stage",
    "format": "str"
  },
  {
    "name": "primary_product_categories",
    "description": "Confirmed product categories the company develops that are relevant to Neuland's capabilities.",
    "label": "Product Categories",
    "format": "str"
  },
  {
    "name": "therapeutic_areas",
    "description": "Therapeutic areas the company focuses on, categorized by Neuland's priorities.",
    "label": "Therapeutic Areas",
    "format": "str"
  },
  {
    "name": "regions",
    "description": "Primary markets and regulatory regions where the company operates or targets.",
    "label": "Regions",
    "format": "str"
  },
  {
    "name": "relevance",
    "description": "Relevance score based on Neuland's engagement or interest.",
    "label": "Relevance Score",
    "format": "number"
  },
  {
    "name": "confidence_level",
    "description": "Confidence level regarding the quality and accuracy of the data.",
    "label": "Confidence Level",
    "format": "percentage"
  },
  {
    "name": "justification",
    "description": "Justification or rationale for the organization’s inclusion or scoring.",
    "label": "Justification",
    "format": "str"
  },
  {
    "name": "ownership_and_financials",
    "description": "Company ownership status (e.g., Public, Private) including revenue, funding, or employee count if available.",
    "label": "Ownership & Financials",
    "format": "str"
  },
  {
    "name": "description",
    "description": "Brief summary of the company’s mission, focus, and business model.",
    "label": "Company Description",
    "format": "str"
  },
  {
    "name": "reassessment_triggers",
    "description": "Triggers that warrant reassessing the company (e.g., strategy shift, partnership).",
    "label": "Reassessment Triggers",
    "format": "str"
  },
  {
    "name": "opportunity_score",
    "description": "Numeric score representing the opportunity level with the organization.",
    "label": "Opportunity Score",
    "format": "float"
  },
  {
    "name": "workspace_name",
    "description": "Name of the workspace or account associated with this organization.",
    "label": "Workspace Name",
    "format": "str"
  }
]
