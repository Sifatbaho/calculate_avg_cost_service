from db.connection import get_cursor

def get_ads_with_avg_price(
    brand=None,
    model=None,
    condition=None,
    manufacture_year=None,
    mileage=None,
    color=None,
    complication=None,
    region=None,
    district=None,
    category=None,
    date_from=None,
    date_to=None,
):
    conn, cur = get_cursor()

    COMPLICATION_FIELD_ID = 42

    conditions = ["1=1", "a.ad_type = 'AUTO'"]
    params = []

    def to_int(val):
        try:
            return int(val) if val not in (None, "", "null") else None
        except (ValueError, TypeError):
            return None

    def to_float(val):
        try:
            return float(val) if val not in (None, "", "null") else None
        except (ValueError, TypeError):
            return None

    def to_str(val):
        return val.strip() if val and val.strip() not in ("", "null") else None

    date_from = to_str(date_from)
    if date_from is not None:
        conditions.append("a.created_at >= %s")
        params.append(date_from)

    date_to = to_str(date_to)
    if date_to is not None:
        conditions.append("a.created_at <= %s")
        params.append(date_to)

    brand = to_str(brand)
    if brand is not None:
        conditions.append("b.name = %s")
        params.append(brand)

    model = to_str(model)
    if model is not None:
        conditions.append("bm.name = %s")
        params.append(model)

    region = to_str(region)
    if region is not None:
        conditions.append("r.name = %s")
        params.append(region)

    district = to_str(district)
    if district is not None:
        conditions.append("d.name = %s")
        params.append(district)

    category = to_str(category)
    if category is not None:
        conditions.append("cat.name = %s")
        params.append(category)

    condition = to_str(condition)
    if condition is not None:
        conditions.append("vc.name = %s")
        params.append(condition)

    manufacture_year = to_int(manufacture_year)
    if manufacture_year is not None:
        conditions.append("vd.year = %s")
        params.append(manufacture_year)

    mileage = to_int(mileage)
    if mileage is not None:
        conditions.append("vd.mileage = %s")
        params.append(mileage)

    color = to_str(color)
    if color is not None:
        conditions.append("vd.vehicle_color = %s")
        params.append(color)

    complication = to_str(complication)
    if complication is not None:
        conditions.append("""
            EXISTS (
                SELECT 1 FROM ad_attribute aa
                WHERE aa.ad_id = a.id
                  AND aa.field_id = %s
                  AND aa.value = %s
            )
        """)
        params.append(COMPLICATION_FIELD_ID)
        params.append(complication)

    where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT
            a.id,
            a.title,
            a.price,
            bm.name                         AS model_name,
            COALESCE(
                ARRAY_AGG(ai.image ORDER BY ai.id) FILTER (WHERE ai.image IS NOT NULL),
                ARRAY[]::varchar[]
            )                               AS images,
            AVG(a.price) OVER (PARTITION BY NULL) AS avg_price,
            COUNT(*) OVER ()                AS total_count

        FROM ad a
        LEFT JOIN brand             b    ON b.id   = a.brand_id
        LEFT JOIN brand_model       bm   ON bm.id  = a.brand_model_id
        LEFT JOIN region            r    ON r.id   = a.region_id
        LEFT JOIN district          d    ON d.id   = a.district_id
        LEFT JOIN category          cat  ON cat.id = a.category_id
        LEFT JOIN vehicle_ad_detail vd   ON vd.ad_id = a.id
        LEFT JOIN vehicle_condition vc   ON vc.id  = vd.condition_id
        LEFT JOIN ad_image          ai   ON ai.ad_id = a.id

        {where_clause}
        GROUP BY
            a.id, a.title, a.price,
            bm.name,
            r.name, d.name, cat.name,
            vd.year, vd.mileage, vd.vehicle_color,
            vc.name
        ORDER BY a.created_at DESC
    """

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    if not rows:
        return {"avg_price": 0.0, "total_count": 0, "listings": []}

    avg_price   = float(rows[0]["avg_price"])
    total_count = rows[0]["total_count"]

    listings = [
        {
            "id":         str(row["id"]),
            "title":      row["title"],
            "price":      str(row["price"]),
            "model_name": row["model_name"],
            "images":     row["images"],
        }
        for row in rows
    ]

    return {
        "avg_price":   avg_price,
        "total_count": total_count,
        "listings":    listings,
    }
