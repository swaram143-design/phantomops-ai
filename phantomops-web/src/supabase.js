import { createClient } from "@supabase/supabase-js";

const supabaseUrl =
  "https://hngxjzzmkbpzmrhimhgm.supabase.co";

const supabaseKey =
  "sb_publishable_vEahGT3rsEyeqrADDPsqEQ_5O2mbyoa";

export const supabase = createClient(
  supabaseUrl,
  supabaseKey
);