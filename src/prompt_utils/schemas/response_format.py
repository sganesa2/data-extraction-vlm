from pydantic import BaseModel, Field

class LineItem(BaseModel):
    lineitem_id: str = Field(description="Unique identifier for the line item")
    query: str = Field(description="Original query text for the line item")
    part_number: str = Field(description="Part or product number")
    brand: str = Field(description="Brand of the item")
    description: str = Field(description="Detailed description of the item")
    quantity: float = Field(description="Quantity of items ordered")
    uom: str = Field(description="Unit of measurement (e.g., EA, PCS, KG)")
    unit_price: float = Field(description="Price per unit")
    uom_less_query: str = Field(description="Query text with UOM information removed")
    product_metadata: dict = Field(description="Additional metadata like product attributes, key features, etc.")


class DataExtractionSchema(BaseModel):
    vendor: str = Field(description="Name of the vendor/supplier")
    purchase_order_number: str = Field(description="Unique PO reference number")
    job_number: str = Field(description="Associated job or project number")
    job_name: str = Field(description="Name or title of the job/project")
    quote_number: str = Field(description="Reference number for the quote")
    delivery_date: str = Field(description="Expected delivery date")
    date_ordered: str = Field(description="Date when the order was placed")
    shipping_instructions: str = Field(description="Special instructions for shipping")
    payment_terms: str = Field(description="Terms and conditions for payment")
    ship_to: str = Field(description="Shipping destination address")
    bill_to: str = Field(description="Billing address")
    shipping_contact: str = Field(description="Contact person for shipping")
    buyer_contact: str = Field(description="Contact person from buying organization")
    notes: str = Field(description="Additional notes or comments")
    ship_via: str = Field(description="Preferred shipping method or carrier")
    line_items: list[LineItem] = Field(description="List of items being ordered")