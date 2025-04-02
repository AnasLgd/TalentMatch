
import React, { useState } from "react";
import { 
  Search, 
  Plus, 
  Filter, 
  ArrowUpDown, 
  MoreVertical, 
  Edit, 
  Trash2, 
  FileText,
  Building,
  Calendar,
  Share2
} from "lucide-react";
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
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

interface Tender {
  id: number;
  title: string;
  client: string;
  requiredSkills: string[];
  location: string;
  endDate: string;
  status: "Nouveau" | "En cours" | "En attente" | "Fermé";
}

const tenders: Tender[] = [
  { id: 1, title: "Développeur React/Node", client: "Société ABC", requiredSkills: ["React", "Node.js", "MongoDB"], location: "Paris", endDate: "15/07/2023", status: "Nouveau" },
  { id: 2, title: "Scrum Master", client: "Entreprise XYZ", requiredSkills: ["Agile", "Jira", "Scrum"], location: "Lyon", endDate: "22/07/2023", status: "En cours" },
  { id: 3, title: "Architecte Cloud", client: "Groupe DEF", requiredSkills: ["AWS", "Azure", "Terraform"], location: "Bordeaux", endDate: "30/07/2023", status: "En cours" },
  { id: 4, title: "Data Engineer", client: "Société MNO", requiredSkills: ["Spark", "Hadoop", "Python"], location: "Nantes", endDate: "05/08/2023", status: "En attente" },
  { id: 5, title: "Chef de projet IT", client: "Entreprise GHI", requiredSkills: ["Prince2", "MS Project", "Agile"], location: "Toulouse", endDate: "12/08/2023", status: "Nouveau" },
  { id: 6, title: "Développeur Java/Spring", client: "Société JKL", requiredSkills: ["Java", "Spring", "Hibernate"], location: "Lille", endDate: "18/08/2023", status: "En cours" },
  { id: 7, title: "UX/UI Designer", client: "Entreprise PQR", requiredSkills: ["Figma", "Sketch", "Adobe XD"], location: "Marseille", endDate: "25/08/2023", status: "Fermé" },
  { id: 8, title: "DevOps Engineer", client: "Groupe STU", requiredSkills: ["Docker", "Kubernetes", "CI/CD"], location: "Strasbourg", endDate: "01/09/2023", status: "En attente" },
];

const getStatusColor = (status: Tender["status"]) => {
  switch (status) {
    case "Nouveau":
      return "bg-blue-500/20 text-blue-500";
    case "En cours":
      return "bg-green-500/20 text-green-500";
    case "En attente":
      return "bg-amber-500/20 text-amber-500";
    case "Fermé":
      return "bg-red-500/20 text-red-500";
    default:
      return "bg-gray-500/20 text-gray-500";
  }
};

const Tenders = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredTenders, setFilteredTenders] = useState(tenders);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    
    if (term.trim() === "") {
      setFilteredTenders(tenders);
    } else {
      const filtered = tenders.filter(
        (tender) =>
          tender.title.toLowerCase().includes(term) ||
          tender.client.toLowerCase().includes(term) ||
          tender.requiredSkills.some((skill) => skill.toLowerCase().includes(term))
      );
      setFilteredTenders(filtered);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Appels d'offres</h1>
        <p className="text-muted-foreground">
          Gérez vos appels d'offres et trouvez les profils correspondants.
        </p>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative max-w-md w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Rechercher par titre, client..."
            className="pl-10"
            value={searchTerm}
            onChange={handleSearch}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Nouvel appel d'offres
          </Button>
        </div>
      </div>

      <Card className="border-border/40">
        <div className="relative w-full overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[300px]">
                  <div className="flex items-center">
                    Titre
                    <ArrowUpDown className="ml-1 h-3 w-3" />
                  </div>
                </TableHead>
                <TableHead>
                  <div className="flex items-center">
                    Client
                    <ArrowUpDown className="ml-1 h-3 w-3" />
                  </div>
                </TableHead>
                <TableHead>Compétences requises</TableHead>
                <TableHead>Localisation</TableHead>
                <TableHead>Date de fin</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredTenders.map((tender) => (
                <TableRow key={tender.id}>
                  <TableCell className="font-medium">{tender.title}</TableCell>
                  <TableCell>{tender.client}</TableCell>
                  <TableCell>
                    <div className="flex flex-wrap gap-1">
                      {tender.requiredSkills.map((skill, idx) => (
                        <Badge key={idx} variant="secondary">{skill}</Badge>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>{tender.location}</TableCell>
                  <TableCell>{tender.endDate}</TableCell>
                  <TableCell>
                    <span className={`inline-flex rounded-full px-2 py-1 text-xs ${getStatusColor(tender.status)}`}>
                      {tender.status}
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
                        <DropdownMenuItem>
                          <FileText className="mr-2 h-4 w-4" />
                          <span>Détails</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Edit className="mr-2 h-4 w-4" />
                          <span>Modifier</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Building className="mr-2 h-4 w-4" />
                          <span>Voir le client</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Calendar className="mr-2 h-4 w-4" />
                          <span>Planifier une réunion</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Share2 className="mr-2 h-4 w-4" />
                          <span>Partager</span>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="text-red-500">
                          <Trash2 className="mr-2 h-4 w-4" />
                          <span>Supprimer</span>
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
  );
};

export default Tenders;
