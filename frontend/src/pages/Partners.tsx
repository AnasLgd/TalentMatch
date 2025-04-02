
import React, { useState } from "react";
import { Search, Plus, Users, Building, Phone, Mail, Link2, MoreVertical, ArrowUpDown, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Partner {
  id: number;
  name: string;
  logo: string;
  consultants: number;
  specialties: string[];
  location: string;
  status: "Actif" | "En attente" | "Inactif";
  contactPerson?: string;
  email?: string;
  phone?: string;
  website?: string;
  collaborations?: number;
}

const partners: Partner[] = [
  {
    id: 1,
    name: "TechConsult",
    logo: "TC",
    consultants: 56,
    specialties: ["Développement", "DevOps", "UX/UI"],
    location: "Paris",
    status: "Actif",
    contactPerson: "Marie Dubois",
    email: "contact@techconsult.fr",
    phone: "01 23 45 67 89",
    website: "techconsult.fr",
    collaborations: 12
  },
  {
    id: 2,
    name: "DataSphere",
    logo: "DS",
    consultants: 32,
    specialties: ["Data Science", "IA", "Big Data"],
    location: "Lyon",
    status: "Actif",
    contactPerson: "Pierre Martin",
    email: "info@datasphere.com",
    phone: "04 56 78 90 12",
    website: "datasphere.com",
    collaborations: 8
  },
  {
    id: 3,
    name: "CloudWorks",
    logo: "CW",
    consultants: 48,
    specialties: ["Cloud", "DevOps", "Infrastructure"],
    location: "Bordeaux",
    status: "Actif",
    contactPerson: "Julie Leroy",
    email: "contact@cloudworks.fr",
    phone: "05 67 89 01 23",
    website: "cloudworks.fr",
    collaborations: 15
  },
  {
    id: 4,
    name: "AgileConsulting",
    logo: "AC",
    consultants: 24,
    specialties: ["Agile", "Scrum", "Management"],
    location: "Nantes",
    status: "En attente",
    contactPerson: "Thomas Bernard",
    email: "info@agileconsulting.fr",
    phone: "02 34 56 78 90",
    website: "agileconsulting.fr"
  },
  {
    id: 5,
    name: "SecureIT",
    logo: "SI",
    consultants: 18,
    specialties: ["Cybersécurité", "Audit", "Conformité"],
    location: "Toulouse",
    status: "Inactif",
    contactPerson: "Sophie Moreau",
    email: "contact@secureit.com",
    phone: "05 12 34 56 78",
    website: "secureit.com",
    collaborations: 3
  },
];

const getStatusColor = (status: Partner["status"]) => {
  switch (status) {
    case "Actif":
      return "bg-green-500/20 text-green-500";
    case "En attente":
      return "bg-amber-500/20 text-amber-500";
    case "Inactif":
      return "bg-red-500/20 text-red-500";
    default:
      return "bg-gray-500/20 text-gray-500";
  }
};

const getLogoColor = (name: string) => {
  const colors = [
    "bg-blue-500/20 text-blue-500",
    "bg-purple-500/20 text-purple-500",
    "bg-green-500/20 text-green-500",
    "bg-amber-500/20 text-amber-500",
    "bg-red-500/20 text-red-500"
  ];
  
  // Simple hash function to consistently get same color for same name
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  return colors[Math.abs(hash) % colors.length];
};

const Partners = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredPartners, setFilteredPartners] = useState(partners);
  const [selectedPartner, setSelectedPartner] = useState<Partner | null>(null);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    
    if (term.trim() === "") {
      setFilteredPartners(partners);
    } else {
      const filtered = partners.filter(
        (partner) =>
          partner.name.toLowerCase().includes(term) ||
          partner.location.toLowerCase().includes(term) ||
          partner.specialties.some((specialty) => specialty.toLowerCase().includes(term))
      );
      setFilteredPartners(filtered);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">ESN Partenaires</h1>
        <p className="text-muted-foreground">
          Gérez vos partenariats avec d'autres ESN pour maximiser les opportunités.
        </p>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative max-w-md w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Rechercher par nom, spécialité..."
            className="pl-10"
            value={searchTerm}
            onChange={handleSearch}
          />
        </div>
        
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Ajouter un partenaire
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card className="border-border/40">
            <div className="relative w-full overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[250px]">
                      <div className="flex items-center">
                        ESN
                        <ArrowUpDown className="ml-1 h-3 w-3" />
                      </div>
                    </TableHead>
                    <TableHead>Consultants</TableHead>
                    <TableHead>Spécialités</TableHead>
                    <TableHead>Localisation</TableHead>
                    <TableHead>Statut</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPartners.map((partner) => (
                    <TableRow 
                      key={partner.id} 
                      className={selectedPartner?.id === partner.id ? "bg-accent/30" : ""}
                      onClick={() => setSelectedPartner(partner)}
                    >
                      <TableCell className="font-medium">
                        <div className="flex items-center gap-2">
                          <div className={`h-8 w-8 rounded-full flex items-center justify-center ${getLogoColor(partner.name)}`}>
                            <span className="text-xs font-medium">{partner.logo}</span>
                          </div>
                          <span>{partner.name}</span>
                        </div>
                      </TableCell>
                      <TableCell>{partner.consultants}</TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {partner.specialties.map((specialty, idx) => (
                            <Badge key={idx} variant="secondary">{specialty}</Badge>
                          ))}
                        </div>
                      </TableCell>
                      <TableCell>{partner.location}</TableCell>
                      <TableCell>
                        <span className={`inline-flex rounded-full px-2 py-1 text-xs ${getStatusColor(partner.status)}`}>
                          {partner.status}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon">
                              <MoreVertical className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => setSelectedPartner(partner)}>
                              Voir les détails
                            </DropdownMenuItem>
                            <DropdownMenuItem>Modifier</DropdownMenuItem>
                            <DropdownMenuItem>Partager des profils</DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem>
                              {partner.status === "Actif" ? "Désactiver" : "Activer"}
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </Card>
        </div>

        <div>
          {selectedPartner ? (
            <Card className="border-border/40 sticky top-20">
              <CardHeader className="flex flex-row items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <div className={`h-10 w-10 rounded-full flex items-center justify-center ${getLogoColor(selectedPartner.name)}`}>
                      <span className="text-sm font-medium">{selectedPartner.logo}</span>
                    </div>
                    <CardTitle>{selectedPartner.name}</CardTitle>
                  </div>
                  <CardDescription>
                    {selectedPartner.location} · {selectedPartner.consultants} consultants
                  </CardDescription>
                </div>
                <span className={`inline-flex rounded-full px-3 py-1 text-xs ${getStatusColor(selectedPartner.status)}`}>
                  {selectedPartner.status}
                </span>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-2">Contact</h3>
                  <div className="space-y-3">
                    <div className="flex items-center">
                      <Users className="h-4 w-4 text-muted-foreground mr-2" />
                      <span>{selectedPartner.contactPerson}</span>
                    </div>
                    <div className="flex items-center">
                      <Mail className="h-4 w-4 text-muted-foreground mr-2" />
                      <a href={`mailto:${selectedPartner.email}`} className="text-primary hover:underline">
                        {selectedPartner.email}
                      </a>
                    </div>
                    <div className="flex items-center">
                      <Phone className="h-4 w-4 text-muted-foreground mr-2" />
                      <span>{selectedPartner.phone}</span>
                    </div>
                    <div className="flex items-center">
                      <Link2 className="h-4 w-4 text-muted-foreground mr-2" />
                      <a href={`https://${selectedPartner.website}`} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                        {selectedPartner.website}
                      </a>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-2">Spécialités</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedPartner.specialties.map((specialty, idx) => (
                      <Badge key={idx} variant="secondary">{specialty}</Badge>
                    ))}
                  </div>
                </div>

                {selectedPartner.collaborations !== undefined && (
                  <div>
                    <h3 className="text-sm font-medium text-muted-foreground mb-2">Collaborations</h3>
                    <div className="flex items-center">
                      <div className="flex items-center">
                        <CheckCircle2 className="h-4 w-4 text-green-500 mr-2" />
                        <span>{selectedPartner.collaborations} projets réalisés ensemble</span>
                      </div>
                    </div>
                  </div>
                )}

                <div className="pt-4 grid grid-cols-2 gap-3">
                  <Button variant="outline" className="w-full">
                    <Building className="mr-2 h-4 w-4" />
                    Voir l'ESN
                  </Button>
                  <Button className="w-full">
                    <Users className="mr-2 h-4 w-4" />
                    Consultants
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="border-border/40 p-8 text-center">
              <div className="flex flex-col items-center justify-center space-y-3">
                <div className="bg-muted p-4 rounded-full">
                  <Building className="h-10 w-10 text-muted-foreground" />
                </div>
                <h3 className="text-lg font-medium">Sélectionnez un partenaire</h3>
                <p className="text-muted-foreground">
                  Cliquez sur une ESN pour afficher ses détails et gérer votre partenariat.
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default Partners;
