CREATE TABLE IF NOT EXISTS listings_for_sale (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    price TEXT NOT NULL,
    price_numeric NUMERIC NOT NULL DEFAULT 0,
    price_label TEXT NOT NULL DEFAULT 'Gross Price',
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    beds TEXT NOT NULL,
    baths TEXT NOT NULL,
    area TEXT NOT NULL,
    img_url TEXT NOT NULL,
    featured BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS listings_pre_selling (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    price TEXT NOT NULL,
    price_numeric NUMERIC NOT NULL DEFAULT 0,
    price_label TEXT NOT NULL DEFAULT 'Starting Price',
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    beds TEXT NOT NULL,
    baths TEXT NOT NULL,
    area TEXT NOT NULL,
    img_url TEXT NOT NULL,
    developer TEXT NOT NULL,
    turnover TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS listings_for_lease (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    price TEXT NOT NULL,
    price_numeric NUMERIC NOT NULL DEFAULT 0,
    price_label TEXT NOT NULL DEFAULT '/ month',
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    beds TEXT NOT NULL,
    baths TEXT NOT NULL,
    area TEXT NOT NULL,
    img_url TEXT NOT NULL,
    furnishing TEXT NOT NULL DEFAULT 'Unfurnished',
    featured BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    interest TEXT NOT NULL DEFAULT '',
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now()
);





-----------------



CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_updated_at_for_sale
    BEFORE UPDATE ON listings_for_sale
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_updated_at_pre_selling
    BEFORE UPDATE ON listings_pre_selling
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_updated_at_for_lease
    BEFORE UPDATE ON listings_for_lease
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();




-----------------


-- Enable RLS
ALTER TABLE listings_for_sale ENABLE ROW LEVEL SECURITY;
ALTER TABLE listings_pre_selling ENABLE ROW LEVEL SECURITY;
ALTER TABLE listings_for_lease ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;

-- PUBLIC READ (frontend listings)
CREATE POLICY "Public read for_sale"
ON listings_for_sale
FOR SELECT
USING (true);

CREATE POLICY "Public read pre_selling"
ON listings_pre_selling
FOR SELECT
USING (true);

CREATE POLICY "Public read for_lease"
ON listings_for_lease
FOR SELECT
USING (true);

-- PUBLIC INSERT (contact form)
CREATE POLICY "Public can insert contact messages"
ON contact_messages
FOR INSERT
TO anon
WITH CHECK (true);

-- ADMIN / SERVICE ROLE FULL ACCESS
CREATE POLICY "Service full access for_sale"
ON listings_for_sale
FOR ALL
USING (auth.role() = 'service_role');

CREATE POLICY "Service full access pre_selling"
ON listings_pre_selling
FOR ALL
USING (auth.role() = 'service_role');

CREATE POLICY "Service full access for_lease"
ON listings_for_lease
FOR ALL
USING (auth.role() = 'service_role');

CREATE POLICY "Service full access messages"
ON contact_messages
FOR ALL
USING (auth.role() = 'service_role');



