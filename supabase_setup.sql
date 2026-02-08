-- ============================================
-- Luxe Properties - Supabase Setup Script
-- Run this in the Supabase SQL Editor
-- ============================================

-- 1. Create tables

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

-- 2. Auto-update updated_at triggers

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

-- 3. Row Level Security

ALTER TABLE listings_for_sale ENABLE ROW LEVEL SECURITY;
ALTER TABLE listings_pre_selling ENABLE ROW LEVEL SECURITY;
ALTER TABLE listings_for_lease ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;

-- Public read access for listings
CREATE POLICY "Public read for_sale" ON listings_for_sale FOR SELECT USING (true);
CREATE POLICY "Public read pre_selling" ON listings_pre_selling FOR SELECT USING (true);
CREATE POLICY "Public read for_lease" ON listings_for_lease FOR SELECT USING (true);

-- Public insert for contact messages
CREATE POLICY "Public insert messages" ON contact_messages FOR INSERT WITH CHECK (true);

-- Service role full access for all tables
CREATE POLICY "Service full access for_sale" ON listings_for_sale FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service full access pre_selling" ON listings_pre_selling FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service full access for_lease" ON listings_for_lease FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service full access messages" ON contact_messages FOR ALL USING (auth.role() = 'service_role');

-- 4. Storage bucket for property images
-- Run this separately if needed:
-- INSERT INTO storage.buckets (id, name, public) VALUES ('property-images', 'property-images', true);

-- 5. Seed data - For Sale listings

INSERT INTO listings_for_sale (title, price, price_numeric, price_label, description, location, beds, baths, area, img_url, featured) VALUES
('Greenwoods Executive Village', '$36,500,000', 36500000, 'Gross Price', 'Greenwoods Executive Village House & Lot For Sale in Pasig City.', 'Pasig City', '4 Beds', '4.5 Baths', '450 m²', 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600&h=400&fit=crop', true),
('The Grove Condo', '$22,000,000', 22000000, 'Gross Price', 'The Grove Condo For Sale in Pasig City. Premium living.', 'Pasig City', '2 Beds', '2 Baths', '120 m²', 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=600&h=400&fit=crop', true),
('BGC Skyline Penthouse', '$85,000,000', 85000000, 'Gross Price', 'Exclusive penthouse with 360-degree views of the BGC skyline.', 'BGC Taguig', '4 Beds', '5 Baths', '650 m²', 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=600&h=400&fit=crop', true),
('Alabang Hills Mansion', '$45,000,000', 45000000, 'Gross Price', 'Elegant mansion in the prestigious Alabang Hills subdivision.', 'Muntinlupa', '6 Beds', '6 Baths', '800 m²', 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=400&fit=crop', false),
('Rockwell Condo Unit', '$18,500,000', 18500000, 'Gross Price', 'Modern condo unit in the heart of Rockwell Center, Makati.', 'Makati City', '2 Beds', '2 Baths', '95 m²', 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&h=400&fit=crop', false),
('Quezon City Townhouse', '$12,500,000', 12500000, 'Gross Price', 'Brand new townhouse with modern design and smart home features.', 'Quezon City', '3 Beds', '3 Baths', '180 m²', 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=600&h=400&fit=crop', false);

-- Seed data - Pre-Selling listings

INSERT INTO listings_pre_selling (title, price, price_numeric, price_label, description, location, beds, baths, area, img_url, developer, turnover) VALUES
('The Aston Place', '$8,500,000', 8500000, 'Starting Price', 'Premium pre-selling condo in the heart of Makati. Expected turnover 2027.', 'Makati City', 'Studio', '1 Bath', '28 m²', 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600&h=400&fit=crop', 'Ayala Land', '2027'),
('Parkview Grand Tower', '$12,000,000', 12000000, 'Starting Price', 'Luxury high-rise development with park views. Flexible payment terms.', 'BGC Taguig', '2 Beds', '2 Baths', '85 m²', 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=600&h=400&fit=crop', 'Megaworld', '2028'),
('Verdana Homes Laguna', '$6,200,000', 6200000, 'Starting Price', 'Suburban house and lot development with resort-style amenities.', 'Laguna', '3 Beds', '2 Baths', '120 m²', 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600&h=400&fit=crop', 'DMCI Homes', '2027'),
('Skyrise Tower Manila', '$5,800,000', 5800000, 'Starting Price', 'Modern condo living in Manila Bay area. Stunning sunset views.', 'Manila', '1 Bed', '1 Bath', '42 m²', 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=600&h=400&fit=crop', 'SM Development', '2026'),
('The Residences at Eastwood', '$9,800,000', 9800000, 'Starting Price', 'Live, work, and play in Eastwood City. Near IT park and lifestyle centers.', 'Quezon City', '2 Beds', '1 Bath', '56 m²', 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&h=400&fit=crop', 'Megaworld', '2028'),
('Seaview Terraces Cebu', '$4,500,000', 4500000, 'Starting Price', 'Beachfront pre-selling condos with ocean views in Cebu.', 'Cebu City', 'Studio', '1 Bath', '32 m²', 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=600&h=400&fit=crop', 'Robinsons Land', '2029');

-- Seed data - For Lease listings

INSERT INTO listings_for_lease (title, price, price_numeric, price_label, description, location, beds, baths, area, img_url, furnishing, featured) VALUES
('Makati CBD Studio', '$35,000', 35000, '/ month', 'Fully furnished studio in the heart of Makati CBD. Walking distance to offices.', 'Makati City', 'Studio', '1 Bath', '32 m²', 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&h=400&fit=crop', 'Fully Furnished', true),
('BGC 2BR Condo', '$85,000', 85000, '/ month', 'Modern 2-bedroom condo in Fort Bonifacio. Pool, gym, and parking included.', 'BGC Taguig', '2 Beds', '2 Baths', '75 m²', 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=600&h=400&fit=crop', 'Fully Furnished', true),
('Ortigas Office Space', '$150,000', 150000, '/ month', 'Prime commercial office space in Ortigas Center. Ready for occupancy.', 'Ortigas Center', 'Open Plan', '4 Baths', '500 m²', 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&h=400&fit=crop', 'Bare', false),
('Alabang Village House', '$120,000', 120000, '/ month', 'Spacious family home in exclusive Alabang village. Pet-friendly.', 'Muntinlupa', '4 Beds', '3 Baths', '350 m²', 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=400&fit=crop', 'Semi-Furnished', false),
('Eastwood 1BR Unit', '$28,000', 28000, '/ month', 'Cozy 1-bedroom unit near Eastwood Mall. Great for young professionals.', 'Quezon City', '1 Bed', '1 Bath', '36 m²', 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=600&h=400&fit=crop', 'Fully Furnished', false),
('Rockwell 3BR Premium', '$180,000', 180000, '/ month', 'Luxury 3-bedroom unit in Rockwell with premium finishes and views.', 'Makati City', '3 Beds', '3 Baths', '150 m²', 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=600&h=400&fit=crop', 'Fully Furnished', true);

-- 6. Homepage Settings (key-value for editable stats)

CREATE TABLE IF NOT EXISTS homepage_settings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    setting_key TEXT NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    setting_label TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TRIGGER trigger_updated_at_homepage_settings
    BEFORE UPDATE ON homepage_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

ALTER TABLE homepage_settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read homepage_settings" ON homepage_settings FOR SELECT USING (true);
CREATE POLICY "Service full access homepage_settings" ON homepage_settings FOR ALL USING (auth.role() = 'service_role');

-- Seed homepage stats
INSERT INTO homepage_settings (setting_key, setting_value, setting_label) VALUES
('stat_1_number', '2500', 'Properties Listed'),
('stat_2_number', '1800', 'Happy Clients'),
('stat_3_number', '150', 'Expert Agents'),
('stat_4_number', '25', 'Years Experience');
