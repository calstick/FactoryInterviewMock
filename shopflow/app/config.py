"""Application configuration and business constants.

NOTE (tech debt): some of these values are duplicated as magic numbers
inside individual routers instead of being imported from here. See ISSUE-06.
"""

# Sales tax applied to the post-discount subtotal.
TAX_RATE = 0.08

# Bulk discount: orders of a single line item at or above this quantity
# receive a percentage discount on that line.
BULK_DISCOUNT_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.10

# Maximum quantity allowed for a single line item in one order.
MAX_LINE_QUANTITY = 99
