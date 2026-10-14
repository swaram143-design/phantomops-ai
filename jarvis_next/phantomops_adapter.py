from .adapters import Worker, WorkerResult


class PhantomOpsAdapter(Worker):
    name = "phantomops"
    capabilities = {
        "research", "opportunity", "select_target", "proposal",
        "crm_sync", "external_send", "followup_automation",
    }

    def score(self, task):
        goal = str(task.get("goal", "")).lower()
        step = task.get("step", {})
        cap = step.get("capability", "")
        score = 20
        if cap in self.capabilities:
            score += 20
        if any(x in goal for x in ("revenue", "lead", "client", "customer", "prospect", "proposal", "automation")):
            score += 30
        return score

    def _context(self, task):
        context = task.get("context")
        return context if isinstance(context, dict) else {}

    def _items(self, data):
        if not isinstance(data, dict):
            return []
        items = []
        for key in ("opportunities", "leads"):
            if isinstance(data.get(key), list):
                items.extend(x for x in data[key] if isinstance(x, dict))
        return items

    def _pick_target(self, data, goal):
        items = self._items(data)
        if not items:
            return {"company": "Prospect", "need": goal, "recipient": None, "selected_target": None}

        def contacts_for(item):
            contacts = item.get("contacts")
            return [c for c in contacts if isinstance(c, dict)] if isinstance(contacts, list) else []

        def first_email(item):
            for key in ("email", "contact_email", "recipient"):
                if item.get(key):
                    return item[key]
            for contact in contacts_for(item):
                if contact.get("email"):
                    return contact["email"]
            return None

        def score(x):
            s = 3 if first_email(x) else 0
            for key in ("website", "company", "name", "title"):
                s += 1 if x.get(key) else 0
            for key in ("intent", "score", "opportunity_score", "buyer_intent"):
                value = x.get(key)
                if isinstance(value, (int, float)):
                    s += min(float(value), 10)
            return s

        target = max(items, key=score)
        company = target.get("company") or target.get("name") or target.get("title") or "Prospect"
        need = target.get("need") or target.get("description") or target.get("reason") or goal
        return {
            "company": company,
            "need": need,
            "recipient": first_email(target),
            "selected_target": target,
            "selection_score": score(target),
        }

    async def run(self, task):
        try:
            capability = task["step"]["capability"]
            goal = task["goal"]
            context = self._context(task)
            merged = {**context, **task}

            if capability == "research":
                from agents.lead_scraper_agent import LeadScraperAgent
                result = await LeadScraperAgent().execute({"description": goal, **context})
                return WorkerResult(result.get("success", False), result, result.get("error"))

            if capability == "opportunity":
                from agents.opportunity_agent import OpportunityAgent
                result = await OpportunityAgent().execute({"description": goal, **context, **task})
                return WorkerResult(result.get("success", False), result, result.get("error"))

            if capability == "select_target":
                return WorkerResult(True, self._pick_target(merged, goal))

            if capability == "proposal":
                target = merged if merged.get("selected_target") else self._pick_target(merged, goal)
                company = target.get("company", "Prospect")
                need = target.get("need", goal)
                from tools.proposal_engine import proposal_engine
                from tools.pdf_proposal_engine import pdf_proposal_engine
                proposal = proposal_engine.generate_proposal(company, need)
                pdf_path = pdf_proposal_engine.generate_pdf(company, proposal)
                return WorkerResult(True, {**target, "proposal": proposal, "pdf": pdf_path})

            if capability == "crm_sync":
                recipient = merged.get("recipient")
                if not recipient:
                    return WorkerResult(False, error="No verified recipient email is available; refusing CRM sync.")
                from tools.crm_memory import crm_memory
                contact = crm_memory.create_contact(recipient, merged.get("company", "Prospect"))
                crm_memory.update_status(recipient, "proposal_ready")
                return WorkerResult(True, {
                    "crm_synced": True,
                    "crm_id": f"local-crm:{recipient}",
                    "crm_contact": contact,
                })

            if capability == "external_send":
                recipient = merged.get("recipient")
                if not recipient:
                    return WorkerResult(False, error="No verified recipient email is available; refusing to send.")
                from agents.proposal_delivery_agent import ProposalDeliveryAgent
                result = await ProposalDeliveryAgent().execute({
                    "company": merged.get("company", "Prospect"),
                    "need": merged.get("need", goal),
                    "recipient": recipient,
                    **({"proposal": merged["proposal"]} if "proposal" in merged else {}),
                })
                return WorkerResult(result.get("success", False), result, result.get("error"))

            if capability == "followup_automation":
                recipient = merged.get("recipient")
                if not recipient:
                    return WorkerResult(False, error="No verified recipient email is available; refusing follow-up scheduling.")
                from tools.followup_engine import followup_engine
                followup_engine.add_followup(recipient, merged.get("company", "Prospect"))
                return WorkerResult(True, {
                    "followup_scheduled": True,
                    "followup_email": recipient,
                    "followup_company": merged.get("company", "Prospect"),
                })

            return WorkerResult(False, error=f"Unsupported capability: {capability}")
        except Exception as exc:
            return WorkerResult(False, error=str(exc))
